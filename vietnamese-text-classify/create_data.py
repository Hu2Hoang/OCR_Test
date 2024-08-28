import os
from faker import Faker
import random

# Khởi tạo Faker
fake = Faker('vi_VN')

sample_notes = [
    "Sản phẩm này được kiểm tra chất lượng nghiêm ngặt trước khi giao hàng.",
    "Đơn hàng này đã được xác nhận và sẽ được giao trong thời gian sớm nhất.",
    "Vui lòng kiểm tra tình trạng hàng hóa ngay khi nhận hàng.",
    "Chúng tôi cam kết cung cấp dịch vụ khách hàng tốt nhất.",
    "Cảm ơn bạn đã chọn mua sản phẩm của chúng tôi.",
    "Nếu có bất kỳ thắc mắc nào, vui lòng liên hệ với chúng tôi ngay.",
    "Hóa đơn này là bằng chứng hợp lệ cho việc mua hàng của bạn.",
    "Chúng tôi hy vọng bạn hài lòng với sản phẩm và dịch vụ của chúng tôi.",
    "Đảm bảo rằng thông tin trên hóa đơn là chính xác trước khi thanh toán.",
    "Nếu có lỗi hoặc vấn đề với sản phẩm, vui lòng liên hệ ngay để được hỗ trợ."
]

# Danh sách các câu tiếng Việt mẫu cho phần ghi chú
financial_report_notes = [
    "Báo cáo tài chính này cung cấp cái nhìn tổng quan về tình hình tài chính của ngân hàng.",
    "Tất cả các số liệu trong báo cáo này đã được kiểm tra và xác nhận.",
    "Doanh thu và chi phí được báo cáo dựa trên các giao dịch thực tế trong năm.",
    "Lợi nhuận và tài sản của ngân hàng đều được tính toán chính xác.",
    "Vốn chủ sở hữu của ngân hàng được cập nhật theo các điều chỉnh gần đây.",
    "Nếu cần thêm thông tin chi tiết, vui lòng liên hệ với phòng kế toán.",
    "Báo cáo này là tài liệu quan trọng cho các cổ đông và nhà đầu tư.",
    "Mọi số liệu trong báo cáo đều tuân theo chuẩn mực kế toán hiện hành.",
    "Chúng tôi cam kết tính chính xác và minh bạch trong báo cáo tài chính này.",
    "Nếu phát hiện sai sót hoặc có bất kỳ câu hỏi nào, vui lòng liên hệ với chúng tôi."
]

marriage_contract_terms = [
    "Hai bên cam kết chung sống hòa thuận và xây dựng gia đình hạnh phúc.",
    "Hai bên sẽ cùng nhau chăm sóc và nuôi dưỡng con cái nếu có.",
    "Mỗi bên đều có quyền và nghĩa vụ như nhau trong việc quản lý tài sản chung.",
    "Hai bên đồng ý hỗ trợ nhau về mặt tài chính và tinh thần trong suốt thời gian hôn nhân.",
    "Mọi tranh chấp phát sinh trong quá trình hôn nhân sẽ được giải quyết qua thương lượng hoặc trọng tài.",
    "Hai bên cam kết không can thiệp vào quyền tự do cá nhân của nhau.",
    "Hợp đồng này có hiệu lực từ ngày ký và không thay đổi nếu không có sự đồng ý của cả hai bên.",
    "Nếu một bên muốn ly hôn, phải thông báo cho bên kia ít nhất 3 tháng trước khi thực hiện thủ tục pháp lý.",
    "Hai bên đồng ý phân chia tài sản chung theo nguyên tắc công bằng và hợp lý.",
    "Mọi điều khoản trong hợp đồng đều tuân theo quy định của pháp luật hiện hành."
]

employment_contract_terms = [
    "Nhân viên cam kết thực hiện đầy đủ nhiệm vụ được giao và tuân thủ quy định của công ty.",
    "Mức lương và các khoản phụ cấp sẽ được trả theo chính sách của công ty và theo quy định của hợp đồng.",
    "Nhân viên phải hoàn thành công việc theo tiêu chuẩn chất lượng và thời gian quy định.",
    "Mọi thay đổi về công việc, địa điểm làm việc sẽ được thông báo trước ít nhất 30 ngày.",
    "Hợp đồng có thể được gia hạn hoặc thay đổi theo thỏa thuận giữa hai bên.",
    "Công ty có quyền sa thải nhân viên nếu nhân viên vi phạm các quy định của công ty hoặc không hoàn thành nhiệm vụ.",
    "Nhân viên có quyền yêu cầu bồi thường theo quy định của pháp luật trong trường hợp hợp đồng bị chấm dứt bất hợp pháp.",
    "Nhân viên có trách nhiệm bảo mật thông tin và tài sản của công ty trong suốt thời gian làm việc.",
    "Công ty có quyền yêu cầu nhân viên làm việc ngoài giờ hoặc vào ngày nghỉ lễ nếu cần thiết.",
    "Mọi tranh chấp phát sinh từ hợp đồng sẽ được giải quyết theo quy định của pháp luật hiện hành."
]

# Hàm tạo một mẫu ngẫu nhiên cho mặt trước của căn cước công dân
def generate_random_cccd():
    return {
        'Số CCCD': fake.unique.random_number(digits=12),
        'Họ và tên': fake.name(),
        'Ngày, tháng, năm sinh': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d/%m/%Y'),
        'Giới tính': random.choice(['Nam', 'Nữ']),
        'Quốc tịch': 'Việt Nam',
        'Quê quán': fake.city(),
        'Nơi thường trú': fake.address(),
        'Ngày cấp': fake.date_this_century(before_today=True, after_today=False).strftime('%d/%m/%Y'),
        'Ngày hết hạn': fake.date_between(start_date='today', end_date='+15y').strftime('%d/%m/%Y'),
        'Chữ ký người cấp': fake.name()
    }

# Hàm tạo một mẫu ngẫu nhiên cho hộ chiếu với các tiêu đề bằng tiếng Anh
def generate_random_passport():
    return {
        'Passport Number': fake.unique.random_number(digits=8),
        'Full Name': fake.name(),
        'Date of Birth': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d/%m/%Y'),
        'Gender': random.choice(['Male', 'Female']),
        'Nationality': 'Vietnam',
        'Place of Birth': fake.city(),
        'Date of Issue': fake.date_this_century(before_today=True, after_today=False).strftime('%d/%m/%Y'),
        'Date of Expiry': fake.date_between(start_date='today', end_date='+10y').strftime('%d/%m/%Y'),
        'Issuing Authority': 'Immigration Department'
    }

# Hàm tạo một mẫu ngẫu nhiên cho sao kê tài sản
def generate_random_asset_statement():
    return {
        'Asset ID': fake.unique.random_number(digits=10),
        'Owner Name': fake.name(),
        'Asset Type': random.choice(['House', 'Car', 'Land', 'Savings']),
        'Asset Value': f"{fake.random_number(digits=9)} VND",
        'Date of Acquisition': fake.date_this_decade(before_today=True, after_today=False).strftime('%d/%m/%Y'),
        'Location': fake.address(),
        'Issuer': fake.company()
    }

# Hàm tạo một mẫu ngẫu nhiên cho sao kê ngân hàng với các tiêu đề bằng tiếng Việt
def generate_random_bank_statement():
    return {
        'Số tài khoản': fake.unique.random_number(digits=10),
        'Chủ tài khoản': fake.name(),
        'Tên ngân hàng': fake.company(),
        'Chi nhánh': fake.city(),
        'Số dư': f"{fake.random_number(digits=9)} VND",
        'Ngày sao kê': fake.date_this_month().strftime('%d/%m/%Y'),
        'Giao dịch': [
            {
                'Ngày': fake.date_this_month().strftime('%d/%m/%Y'),
                'Mô tả': fake.sentence(nb_words=6),
                'Số tiền': f"{fake.random_number(digits=7)} VND",
                'Loại': random.choice(['Ghi có', 'Ghi nợ'])
            } for _ in range(random.randint(5, 10))
        ]
    }

# Hàm tạo một mẫu ngẫu nhiên cho báo cáo tài chính ngân hàng
def generate_random_financial_report():
    return {
        'Số báo cáo': fake.unique.random_number(digits=8),
        'Tên ngân hàng': fake.company(),
        'Ngày báo cáo': fake.date_this_year().strftime('%d/%m/%Y'),
        'Doanh thu': f"{fake.random_number(digits=10)} VND",
        'Chi phí': f"{fake.random_number(digits=10)} VND",
        'Lợi nhuận': f"{fake.random_number(digits=10)} VND",
        'Tài sản': f"{fake.random_number(digits=10)} VND",
        'Nợ phải trả': f"{fake.random_number(digits=10)} VND",
        'Vốn chủ sở hữu': f"{fake.random_number(digits=10)} VND",
        'Ghi chú': random.choice(financial_report_notes)
    }

# Hàm tạo một mẫu ngẫu nhiên cho hợp đồng lao động
def generate_random_employment_contract():
    return {
        'Số hợp đồng': fake.unique.random_number(digits=8),
        'Tên công ty': fake.company(),
        'Tên nhân viên': fake.name(),
        'Chức vụ': random.choice(['Nhân viên', 'Quản lý', 'Trưởng phòng', 'Giám đốc']),
        'Ngày ký hợp đồng': fake.date_this_year().strftime('%d/%m/%Y'),
        'Ngày bắt đầu': fake.date_this_year().strftime('%d/%m/%Y'),
        'Ngày kết thúc': fake.date_between(start_date='+1y', end_date='+5y').strftime('%d/%m/%Y'),
        'Mức lương': f"{fake.random_number(digits=6)} VND",
        'Địa điểm làm việc': fake.address(),
        'Điều khoản': random.choice(employment_contract_terms)
    }

# Hàm tạo một mẫu ngẫu nhiên cho hợp đồng hôn nhân
def generate_random_marriage_contract():
    return {
        'Số hợp đồng': fake.unique.random_number(digits=8),
        'Tên người chồng': fake.name(),
        'Tên người vợ': fake.name(),
        'Ngày kết hôn': fake.date_this_year().strftime('%d/%m/%Y'),
        'Địa điểm kết hôn': fake.city(),
        'Số CCCD của người chồng': fake.unique.random_number(digits=12),
        'Số CCCD của người vợ': fake.unique.random_number(digits=12),
        'Quốc tịch của người chồng': 'Việt Nam',
        'Quốc tịch của người vợ': 'Việt Nam',
        'Địa chỉ thường trú của người chồng': fake.address(),
        'Địa chỉ thường trú của người vợ': fake.address(),
        'Điều khoản': random.choice(marriage_contract_terms) 
    }

# Hàm tạo một mẫu ngẫu nhiên cho hóa đơn bán hàng điện tử
def generate_random_e_invoice():
    return {
        'Mã hóa đơn': fake.unique.random_number(digits=10),
        'Tên người mua': fake.name(),
        'Tên người bán': fake.company(),
        'Địa chỉ người mua': fake.address(),
        'Địa chỉ người bán': fake.address(),
        'Ngày lập hóa đơn': fake.date_this_month().strftime('%d/%m/%Y'),
        'Ngày giao hàng': fake.date_this_month().strftime('%d/%m/%Y'),
        'Danh sách sản phẩm': [
            {
                'Tên sản phẩm': fake.word(),
                'Số lượng': random.randint(1, 10),
                'Đơn giá': f"{fake.random_number(digits=5)} VND",
                'Thành tiền': f"{fake.random_number(digits=6)} VND"
            } for _ in range(random.randint(1, 5))
        ],
        'Tổng tiền': f"{fake.random_number(digits=6)} VND",
        'Thuế VAT': f"{fake.random_number(digits=4)} VND",
        'Tổng thanh toán': f"{fake.random_number(digits=6) + fake.random_number(digits=4)} VND",
        'Ghi chú': random.choice(sample_notes)
    }

# Hàm tạo một mẫu ngẫu nhiên cho đơn chứng từ tài sản
def generate_random_asset_document():
    return {
        'Mã chứng từ': fake.unique.random_number(digits=10),
        'Tên người sở hữu': fake.name(),
        'Loại tài sản': random.choice(['Nhà', 'Xe', 'Đất', 'Tiền gửi']),
        'Giá trị tài sản': f"{fake.random_number(digits=9)} VND",
        'Ngày cấp': fake.date_this_decade(before_today=True, after_today=False).strftime('%d/%m/%Y'),
        'Địa chỉ tài sản': fake.address(),
        'Cơ quan cấp': fake.company(),
        'Mô tả': f"Tài sản này là khoản {random.choice(['nhà', 'xe', 'đất', 'tiền gửi'])} với giá trị {fake.random_number(digits=9)} VND. Được cấp bởi cơ quan {fake.company()} và đã được cấp vào ngày {fake.date_this_decade(before_today=True, after_today=False).strftime('%d/%m/%Y')}."
    }

# Tạo thư mục để lưu các file .txt nếu chưa tồn tại
# os.makedirs('cccd_samples', exist_ok=True)

# Tạo và lưu 1000 mẫu ngẫu nhiên vào các file .txt

# for i in range(1000):
#     # cccd = generate_random_cccd()
#     # filename = f"data_new/CCCD Passport/CCCD_{i+1}.txt"
#     # with open(filename, 'w', encoding='utf-8') as file:
#     #     for key, value in cccd.items():
#     #         file.write(f"{key}: {value}\n")
#     # passport_filename = f"data_new/CCCD Passport/passport_{i+1}.txt"
#     employment_contract = generate_random_employment_contract()
#     employment_contract_filename = f"data_new/Hop dong lao dong/employment_contract_{i+1}.txt"
    
#     with open(employment_contract_filename, 'w', encoding='utf-8') as file:
#         for key, value in employment_contract.items():
#             file.write(f"{key}: {value}\n")

for i in range(500):
    cccd = generate_random_cccd()
    passport = generate_random_passport()
    asset_statement = generate_random_asset_statement()
    bank_statement = generate_random_bank_statement()
    financial_report = generate_random_financial_report()
    employment_contract = generate_random_employment_contract()
    marriage_contract = generate_random_marriage_contract()
    e_invoice = generate_random_e_invoice()
    asset_document = generate_random_asset_document()
    
    cccd_filename = f"data_new/Test_full/CCCD Passport/cccd_{i+1}.txt"
    passport_filename = f"data_new/Test_full/CCCD Passport/passport_{i+1}.txt"
    asset_statement_filename = f"data_new/Test_full/Chung tu tai san/asset_statement_{i+1}.txt"
    bank_statement_filename = f"data_new/Test_full/Sao ke/bank_statement_{i+1}.txt"
    financial_report_filename = f"data_new/Test_full/Bao cao tai chinh/financial_report_{i+1}.txt"
    employment_contract_filename = f"data_new/Test_full/Hop dong lao dong/employment_contract_{i+1}.txt"
    marriage_contract_filename = f"data_new/Test_full/Hop dong hon nhan/marriage_contract_{i+1}.txt"
    e_invoice_filename = f"data_new/Test_full/Hoa don ban hang dien tu/e_invoice_{i+1}.txt"
    asset_document_filename = f"data_new/Test_full/Chung tu tai san/asset_document_{i+1}.txt"

    with open(cccd_filename, 'w', encoding='utf-8') as file:
        for key, value in cccd.items():
            file.write(f"{key}: {value}\n")
    
    with open(passport_filename, 'w', encoding='utf-8') as file:
        for key, value in passport.items():
            file.write(f"{key}: {value}\n")
    
    with open(asset_statement_filename, 'w', encoding='utf-8') as file:
        for key, value in asset_statement.items():
            file.write(f"{key}: {value}\n")
    
    with open(bank_statement_filename, 'w', encoding='utf-8') as file:
        for key, value in bank_statement.items():
            if key == 'Giao dịch':
                file.write(f"{key}:\n")
                for txn in value:
                    file.write("  - ")
                    for txn_key, txn_value in txn.items():
                        file.write(f"{txn_key}: {txn_value}; ")
                    file.write("\n")
            else:
                file.write(f"{key}: {value}\n")
    
    with open(financial_report_filename, 'w', encoding='utf-8') as file:
        for key, value in financial_report.items():
            file.write(f"{key}: {value}\n")

    with open(employment_contract_filename, 'w', encoding='utf-8') as file:
        for key, value in employment_contract.items():
            file.write(f"{key}: {value}\n")
    
    with open(marriage_contract_filename, 'w', encoding='utf-8') as file:
        for key, value in marriage_contract.items():
            file.write(f"{key}: {value}\n")

    with open(e_invoice_filename, 'w', encoding='utf-8') as file:
        for key, value in e_invoice.items():
            if key == 'Danh sách sản phẩm':
                file.write(f"{key}:\n")
                for item in value:
                    file.write("  - ")
                    for item_key, item_value in item.items():
                        file.write(f"{item_key}: {item_value}; ")
                    file.write("\n")
            else:
                file.write(f"{key}: {value}\n")
    
    with open(asset_document_filename, 'w', encoding='utf-8') as file:
        for key, value in asset_document.items():
            file.write(f"{key}: {value}\n")

print("Hoàn thành tạo 1000 mẫu căn cước công dân trong thư mục 'cccd_samples'.")
