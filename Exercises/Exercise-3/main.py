import gzip
import io
import requests
import traceback

class CommonCrawlDownloader:
    """
    Class để xử lý việc tải và xử lý file từ Common Crawl
    """
    def __init__(self):
        """Khởi tạo"""
        self.base_url = "https://data.commoncrawl.org"

    def download_file(self, path):
        """
        Tải file từ Common Crawl qua HTTP
        
        Args:
            path (str): Đường dẫn đến file
            
        Returns:
            bytes: Nội dung của file
        """
        url = f"{self.base_url}/{path}"
        print(f"Downloading file from {url}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error downloading file: {e}")
            raise

    def extract_gz_file(self, gz_content):
        """
        Giải nén file gzip
        
        Args:
            gz_content (bytes): Nội dung file gzip
            
        Returns:
            str: Nội dung đã giải nén
        """
        print("Extracting gzip file")
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(gz_content), mode='rb') as f:
                return f.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f"Error extracting file: {e}")
            raise

    def get_first_line_uri(self, content):
        """
        Trích xuất URI từ dòng đầu tiên của nội dung
        
        Args:
            content (str): Nội dung text
            
        Returns:
            str: URI từ dòng đầu tiên
        """
        first_line = content.strip().split('\n')[0].strip()
        print(f"Found URI in first line: {first_line}")
        return first_line

    def stream_file(self, path, max_lines=100):
        """
        Stream nội dung file từ Common Crawl và in từng dòng
        Giới hạn số dòng được in ra
        
        Args:
            path (str): Đường dẫn đến file
            max_lines (int): Số dòng tối đa để hiển thị
        """
        url = f"{self.base_url}/{path}"
        print(f"Streaming content from {url}")
        print(f"Will display maximum {max_lines} lines")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Đơn giản hóa: Chỉ đọc và in ra từng dòng
            line_count = 0
            for line in response.iter_lines():
                if line:
                    # In ra dòng như nó vốn có
                    try:
                        print(line.decode('utf-8'))
                    except UnicodeDecodeError:
                        # Nếu không thể decode bằng UTF-8, sử dụng latin-1 (sẽ không bao giờ lỗi)
                        print(line.decode('latin-1'))
                    
                    line_count += 1
                    if line_count >= max_lines:
                        print(f"Reached maximum line limit ({max_lines} lines). Stopping.")
                        break
            
            print(f"Total lines processed: {line_count}")
        
        except Exception as e:
            print(f"Error streaming file: {e}")
            raise


class CommonCrawlProcessor:
    """
    Class để xử lý luồng làm việc với dữ liệu Common Crawl
    """
    def __init__(self, max_lines=100):
        """
        Khởi tạo CommonCrawlDownloader
        
        Args:
            max_lines (int): Số dòng tối đa để hiển thị từ file cuối cùng
        """
        self.downloader = CommonCrawlDownloader()
        self.max_lines = max_lines

    def process(self):
        """
        Xử lý chính: tải file gz, giải nén, lấy URI, tải và in nội dung
        """
        try:
            # Bước 1: Tải file wet.paths.gz từ Common Crawl
            initial_path = "crawl-data/CC-MAIN-2022-05/wet.paths.gz"
            gz_content = self.downloader.download_file(initial_path)
            
            # Bước 2: Giải nén file và đọc nội dung
            extracted_content = self.downloader.extract_gz_file(gz_content)
            
            # Bước 3: Lấy URL từ dòng đầu tiên
            uri = self.downloader.get_first_line_uri(extracted_content)
            
            # Bước 4: Stream file từ URI và in từng dòng, giới hạn số dòng
            self.downloader.stream_file(uri, self.max_lines)
            
            return True
            
        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()
            return False


def main():
    """Hàm main để chạy ứng dụng"""
    print("Starting Exercise 3 - AWS S3 + Common Crawl")

    # Số dòng hiển thị
    max_lines = 100
    
    processor = CommonCrawlProcessor(max_lines)
    success = processor.process()
    
    if success:
        print("Exercise 3 completed successfully")
    else:
        print("Exercise 3 failed")
    
    print("Exercise 3 completed")


if __name__ == "__main__":

    main()