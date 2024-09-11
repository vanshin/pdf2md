import os
from pdf2image import convert_from_path, pdfinfo_from_path
from models.pdf import PDFFile
from repositories.pdf import PDFFileRepo
from util import HOME

PDF_IMAGE_PATH = os.path.join(HOME, 'storage', 'pdf_image')


class PDF2Img(object):

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        self.image_path = os.path.join(PDF_IMAGE_PATH, self.pdf_name)
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)

        # 保存新pdf的数据
        info = self.pdf_info()
        pdf_file_repo = PDFFileRepo()
        p = pdf_file_repo.get_by('pdf_name', self.pdf_name)
        if not p:
            p = PDFFile(
                pdf_name=self.pdf_name,
                pdf_page_count=info['pages'],
            )
            pdf_file_repo.add(p)
        self.pdf_id = p.id

    def pdf_info(self):
        """pdf文档的信息"""

        data = pdfinfo_from_path(self.pdf_path)
        data = {k.lower(): v for k, v in data.items()}
        return data

    def exist_pdf_images(self):
        """已经切分的pdf页的图片"""

        images = os.listdir(self.image_path)
        if not images:
            return []

        pdf_image_list = []
        for i in images:
            name = i.lower()
            if not name.endswith(('png', 'jpg', 'jpeg')):
                continue
            name, suffix = i.split('.')
            pdf_image_list.append((int(name), i))

        return pdf_image_list

    def rest_image_range(self, start=None, end=None):
        """剩余还没有切分的pdf图片"""

        if not start:
            start = 1
        if not end:
            end = self.pdf_info()['pages']

        # 已知的具体数字
        pdf_images = self.exist_pdf_images()
        existing_numbers = [i[0] for i in pdf_images]
        existing_range_images = []

        # 找出未被覆盖的区间
        missing_intervals = []
        while start <= end:
            # 如果这个数字不在已存在的集合中
            if start not in existing_numbers:
                missing_start = start
                while start <= end and start not in existing_numbers:
                    start += 1
                missing_end = start - 1
                missing_intervals.append((missing_start, missing_end))
            else:
                existing_range_images.append(start)
                start += 1
        return missing_intervals, existing_range_images

    def convert_pdf_to_image(self, first_page=None, last_page=None):

        # 将PDF文件转换为图像列表
        images = convert_from_path(
            self.pdf_path, dpi=200,
            first_page=first_page,
            last_page=last_page
        )

        res = []
        # 遍历图像列表并保存每个图像
        for i, image in enumerate(images):
            # 构造输出文件名
            output_filename = f"{i+first_page}.png"
            output_filepath = f"{self.image_path}/{output_filename}"

            # 保存图像
            image.save(output_filepath, "PNG")
            res.append(output_filepath)

        return res

    def delete_images(self):
        # 遍历指定文件夹
        for filename in os.listdir(self.image_path):
            file_path = os.path.join(self.image_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或链接
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    def convert_pdf(self, start, end):
        """转换指定范围的pdf为图片"""

        image_paths = []
        intervals, existing_range_images = self.rest_image_range(start, end)
        for i in existing_range_images:
            output_filename = f"{i}.png"
            output_filepath = f"{self.image_path}/{output_filename}"
            image_paths.append(output_filepath)
        for start, end in intervals:
            image_paths.extend(
                self.convert_pdf_to_image(start, end)
            )
        return image_paths
