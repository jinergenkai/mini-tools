import qrcode

class VietQR:
    def __init__(self):
        self.payload_format_indicator = "000201"
        self.point_of_initiation_method = "010212"
        self.consumer_account_information = ""
        self.guid = "0010A000000727"
        self.service_code = "0208QRIBFTTA"
        self.transaction_currency = "5303704"
        self.transaction_amount = ""
        self.country_code = "5802VN"
        self.additional_data_field_template = ""
        self.crc = ""

    def convert_length(self, string):
        num = len(string)
        return f"0{num}" if num < 10 else str(num)

    def set_transaction_amount(self, money):
        length = self.convert_length(money)
        self.transaction_amount = f"54{length}{money}"
        return self

    def set_beneficiary_organization(self, acquier_id, consumer_id):
        acquier_length = self.convert_length(acquier_id)
        acquier = f"00{acquier_length}{acquier_id}"
        consumer_length = self.convert_length(consumer_id)
        consumer = f"01{consumer_length}{consumer_id}"
        beneficiary_organization = f"{acquier}{consumer}"
        beneficiary_organization_length = self.convert_length(beneficiary_organization)
        
        # Calculate the full consumer account information
        consumer_account_information = f"{self.guid}01{beneficiary_organization_length}{beneficiary_organization}{self.service_code}"
        consumer_account_information_length = self.convert_length(consumer_account_information)
        self.consumer_account_information = f"38{consumer_account_information_length}{consumer_account_information}"
        return self

    def set_additional_data_field_template(self, content):
        content_length = self.convert_length(content)
        additional_data = f"08{content_length}{content}"
        additional_data_field_template_length = self.convert_length(additional_data)
        self.additional_data_field_template = f"62{additional_data_field_template_length}{additional_data}"
        return self

    def calc_crc(self, string):
        crc_table = [
            0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7, 0x8108,
            0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef, 0x1231, 0x0210,
            0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6, 0x9339, 0x8318, 0xb37b,
            0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de, 0x2462, 0x3443, 0x0420, 0x1401,
            0x64e6, 0x74c7, 0x44a4, 0x5485, 0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee,
            0xf5cf, 0xc5ac, 0xd58d, 0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6,
            0x5695, 0x46b4, 0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d,
            0xc7bc, 0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
            0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b, 0x5af5,
            0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12, 0xdbfd, 0xcbdc,
            0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a, 0x6ca6, 0x7c87, 0x4ce4,
            0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41, 0xedae, 0xfd8f, 0xcdec, 0xddcd,
            0xad2a, 0xbd0b, 0x8d68, 0x9d49, 0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13,
            0x2e32, 0x1e51, 0x0e70, 0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a,
            0x9f59, 0x8f78, 0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e,
            0xe16f, 0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
            0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e, 0x02b1,
            0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256, 0xb5ea, 0xa5cb,
            0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d, 0x34e2, 0x24c3, 0x14a0,
            0x0481, 0x7466, 0x6447, 0x5424, 0x4405, 0xa7db, 0xb7fa, 0x8799, 0x97b8,
            0xe75f, 0xf77e, 0xc71d, 0xd73c, 0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657,
            0x7676, 0x4615, 0x5634, 0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9,
            0xb98a, 0xa9ab, 0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882,
            0x28a3, 0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
            0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92, 0xfd2e,
            0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9, 0x7c26, 0x6c07,
            0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1, 0xef1f, 0xff3e, 0xcf5d,
            0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8, 0x6e17, 0x7e36, 0x4e55, 0x5e74,
            0x2e93, 0x3eb2, 0x0ed1, 0x1ef0
        ]

        crc = 0xffff
        for char in string:
            c = ord(char)
            if c > 255:
                raise ValueError("Character out of range")
            j = (c ^ (crc >> 8)) & 0xff
            crc = crc_table[j] ^ (crc << 8)

        return crc & 0xffff

    def build(self):
        content_qr = (
            f"{self.payload_format_indicator}{self.point_of_initiation_method}"
            f"{self.consumer_account_information}{self.transaction_currency}"
            f"{self.transaction_amount}{self.country_code}"
            f"{self.additional_data_field_template}6304"
        )
        crc = format(self.calc_crc(content_qr), '04x').upper()
        return f"{content_qr}{crc}"

def get_bin_code(identifier, bank_list):
    for bank in bank_list:
        if bank['bin'] == identifier or bank['shortName'] == identifier:
            return bank['bin']
    raise ValueError(f"Không tìm thấy ngân hàng với shortName hoặc bin: {identifier}")

def get_bank_name(bin_code, bank_list):
    for bank in bank_list:
        if bank['bin'] == bin_code:
            return bank['name']
    return "Unknown Bank"

def generate_qr_code(data, filename="qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

if __name__ == "__main__":
    bank_list = [
        {"id": 17, "name": "Ngân hàng TMCP Công thương Việt Nam", "code": "ICB", "bin": "970415", "shortName": "VietinBank"},
        {"id": 43, "name": "Ngân hàng TMCP Ngoại Thương Việt Nam", "code": "VCB", "bin": "970436", "shortName": "Vietcombank"},
        {"id": 4, "name": "Ngân hàng TMCP Đầu tư và Phát triển Việt Nam", "code": "BIDV", "bin": "970418", "shortName": "BIDV"},
        {"id": 42, "name": "Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam", "code": "VBA", "bin": "970405", "shortName": "Agribank"},
        {"id": 26, "name": "Ngân hàng TMCP Phương Đông", "code": "OCB", "bin": "970448", "shortName": "OCB"},
        {"id": 21, "name": "Ngân hàng TMCP Quân đội", "code": "MB", "bin": "970422", "shortName": "MBBank"},
        {"id": 38, "name": "Ngân hàng TMCP Kỹ thương Việt Nam", "code": "TCB", "bin": "970407", "shortName": "Techcombank"},
        {"id": 2, "name": "Ngân hàng TMCP Á Châu", "code": "ACB", "bin": "970416", "shortName": "ACB"},
        {"id": 47, "name": "Ngân hàng TMCP Việt Nam Thịnh Vượng", "code": "VPB", "bin": "970432", "shortName": "VPBank"},
        {"id": 39, "name": "Ngân hàng TMCP Tiên Phong", "code": "TPB", "bin": "970423", "shortName": "TPBank"},
        {"id": 36, "name": "Ngân hàng TMCP Sài Gòn Thương Tín", "code": "STB", "bin": "970403", "shortName": "Sacombank"},
        {"id": 12, "name": "Ngân hàng TMCP Phát triển Thành phố Hồ Chí Minh", "code": "HDB", "bin": "970437", "shortName": "HDBank"},
        {"id": 44, "name": "Ngân hàng TMCP Bản Việt", "code": "VCCB", "bin": "970454", "shortName": "VietCapitalBank"},
        {"id": 31, "name": "Ngân hàng TMCP Sài Gòn", "code": "SCB", "bin": "970429", "shortName": "SCB"},
        {"id": 45, "name": "Ngân hàng TMCP Quốc tế Việt Nam", "code": "VIB", "bin": "970441", "shortName": "VIB"},
        {"id": 35, "name": "Ngân hàng TMCP Sài Gòn - Hà Nội", "code": "SHB", "bin": "970443", "shortName": "SHB"},
        {"id": 10, "name": "Ngân hàng TMCP Xuất Nhập khẩu Việt Nam", "code": "EIB", "bin": "970431", "shortName": "Eximbank"},
        {"id": 22, "name": "Ngân hàng TMCP Hàng Hải Việt Nam", "code": "MSB", "bin": "970426", "shortName": "MSB"},
        {"id": 53, "name": "TMCP Việt Nam Thịnh Vượng - Ngân hàng số CAKE by VPBank", "code": "CAKE", "bin": "546034", "shortName": "CAKE"},
        {"id": 54, "name": "TMCP Việt Nam Thịnh Vượng - Ngân hàng số Ubank by VPBank", "code": "Ubank", "bin": "546035", "shortName": "Ubank"},
        {"id": 57, "name": "Tổng Công ty Dịch vụ số Viettel - Chi nhánh tập đoàn công nghiệp viễn thông Quân Đội", "code": "VTLMONEY", "bin": "971005", "shortName": "ViettelMoney"},
        {"id": 58, "name": "Ngân hàng số Timo by Ban Viet Bank (Timo by Ban Viet Bank)", "code": "TIMO", "bin": "963388", "shortName": "Timo"},
        {"id": 56, "name": "VNPT Money", "code": "VNPTMONEY", "bin": "971011", "shortName": "VNPTMoney"},
        {"id": 34, "name": "Ngân hàng TMCP Sài Gòn Công Thương", "code": "SGICB", "bin": "970400", "shortName": "SaigonBank"},
        {"id": 3, "name": "Ngân hàng TMCP Bắc Á", "code": "BAB", "bin": "970409", "shortName": "BacABank"},
        {"id": 64, "name": "Ngân hàng TMCP Đại Chúng Việt Nam Ngân hàng số", "code": "PVDB", "bin": "971133", "shortName": "PVcomBank Pay"},
        {"id": 30, "name": "Ngân hàng TMCP Đại Chúng Việt Nam", "code": "PVCB", "bin": "970412", "shortName": "PVcomBank"},
        {"id": 27, "name": "Ngân hàng TNHH MTV Việt Nam Hiện Đại", "code": "MBV", "bin": "970414", "shortName": "MBV"},
        {"id": 24, "name": "Ngân hàng TMCP Quốc Dân", "code": "NCB", "bin": "970419", "shortName": "NCB"},
        {"id": 37, "name": "Ngân hàng TNHH MTV Shinhan Việt Nam", "code": "SHBVN", "bin": "970424", "shortName": "ShinhanBank"},
        {"id": 1, "name": "Ngân hàng TMCP An Bình", "code": "ABB", "bin": "970425", "shortName": "ABBANK"},
        {"id": 41, "name": "Ngân hàng TMCP Việt Á", "code": "VAB", "bin": "970427", "shortName": "VietABank"},
        {"id": 23, "name": "Ngân hàng TMCP Nam Á", "code": "NAB", "bin": "970428", "shortName": "NamABank"},
        {"id": 29, "name": "Ngân hàng TMCP Thịnh vượng và Phát triển", "code": "PGB", "bin": "970430", "shortName": "PGBank"},
        {"id": 46, "name": "Ngân hàng TMCP Việt Nam Thương Tín", "code": "VIETBANK", "bin": "970433", "shortName": "VietBank"},
        {"id": 5, "name": "Ngân hàng TMCP Bảo Việt", "code": "BVB", "bin": "970438", "shortName": "BaoVietBank"},
        {"id": 33, "name": "Ngân hàng TMCP Đông Nam Á", "code": "SEAB", "bin": "970440", "shortName": "SeABank"},
        {"id": 52, "name": "Ngân hàng Hợp tác xã Việt Nam", "code": "COOPBANK", "bin": "970446", "shortName": "COOPBANK"},
        {"id": 20, "name": "Ngân hàng TMCP Lộc Phát Việt Nam", "code": "LPB", "bin": "970449", "shortName": "LPBank"},
        {"id": 19, "name": "Ngân hàng TMCP Kiên Long", "code": "KLB", "bin": "970452", "shortName": "KienLongBank"},
        {"id": 55, "name": "Ngân hàng Đại chúng TNHH Kasikornbank", "code": "KBank", "bin": "668888", "shortName": "KBank"},
        {"id": 62, "name": "Công ty Tài chính TNHH MTV Mirae Asset (Việt Nam)", "code": "MAFC", "bin": "977777", "shortName": "MAFC"},
        {"id": 61, "name": "Ngân hàng KEB Hana – Chi nhánh Hà Nội", "code": "KEBHANAHN", "bin": "970467", "shortName": "KEBHANAHN"},
        {"id": 60, "name": "Ngân hàng KEB Hana – Chi nhánh Thành phố Hồ Chí Minh", "code": "KEBHANAHCM", "bin": "970466", "shortName": "KEBHanaHCM"},
        {"id": 59, "name": "Ngân hàng Citibank, N.A. - Chi nhánh Hà Nội", "code": "CITIBANK", "bin": "533948", "shortName": "Citibank"},
        {"id": 63, "name": "Ngân hàng Chính sách Xã hội", "code": "VBSP", "bin": "999888", "shortName": "VBSP"},
        {"id": 6, "name": "Ngân hàng Thương mại TNHH MTV Xây dựng Việt Nam", "code": "CBB", "bin": "970444", "shortName": "CBBank"},
        {"id": 7, "name": "Ngân hàng TNHH MTV CIMB Việt Nam", "code": "CIMB", "bin": "422589", "shortName": "CIMB"},
        {"id": 8, "name": "DBS Bank Ltd - Chi nhánh Thành phố Hồ Chí Minh", "code": "DBS", "bin": "796500", "shortName": "DBSBank"},
        {"id": 9, "name": "Ngân hàng TNHH MTV Số Vikki", "code": "Vikki", "bin": "970406", "shortName": "Vikki"},
        {"id": 28, "name": "Ngân hàng TNHH MTV Public Việt Nam", "code": "PBVN", "bin": "970439", "shortName": "PublicBank"},
        {"id": 51, "name": "Ngân hàng Kookmin - Chi nhánh Thành phố Hồ Chí Minh", "code": "KBHCM", "bin": "970463", "shortName": "KookminHCM"},
        {"id": 50, "name": "Ngân hàng Kookmin - Chi nhánh Hà Nội", "code": "KBHN", "bin": "970462", "shortName": "KookminHN"},
        {"id": 49, "name": "Ngân hàng TNHH MTV Woori Việt Nam", "code": "WVN", "bin": "970457", "shortName": "Woori"},
        {"id": 48, "name": "Ngân hàng Liên doanh Việt - Nga", "code": "VRB", "bin": "970421", "shortName": "VRB"},
        {"id": 11, "name": "Ngân hàng Thương mại TNHH MTV Dầu Khí Toàn Cầu", "code": "GPB", "bin": "970408", "shortName": "GPBank"},
        {"id": 13, "name": "Ngân hàng TNHH MTV Hong Leong Việt Nam", "code": "HLBVN", "bin": "970442", "shortName": "HongLeong"},
        {"id": 14, "name": "Ngân hàng TNHH MTV HSBC (Việt Nam)", "code": "HSBC", "bin": "458761", "shortName": "HSBC"},
        {"id": 15, "name": "Ngân hàng Công nghiệp Hàn Quốc - Chi nhánh Hà Nội", "code": "IBK - HN", "bin": "970455", "shortName": "IBKHN"},
        {"id": 16, "name": "Ngân hàng Công nghiệp Hàn Quốc - Chi nhánh TP. Hồ Chí Minh", "code": "IBK - HCM", "bin": "970456", "shortName": "IBKHCM"},
        {"id": 25, "name": "Ngân hàng Nonghyup - Chi nhánh Hà Nội", "code": "NHB HN", "bin": "801011", "shortName": "Nonghyup"},
        {"id": 40, "name": "Ngân hàng United Overseas - Chi nhánh TP. Hồ Chí Minh", "code": "UOB", "bin": "970458", "shortName": "UnitedOverseas"},
        {"id": 18, "name": "Ngân hàng TNHH Indovina", "code": "IVB", "bin": "970434", "shortName": "IndovinaBank"},
        {"id": 32, "name": "Ngân hàng TNHH MTV Standard Chartered Bank Việt Nam", "code": "SCVN", "bin": "970410", "shortName": "StandardChartered"}
    ]

    viet_qr = VietQR()
    identifier = "VietinBank"  # Hoặc "970415"
    account_number = "111135888888"
    amount = "100000"
    purpose = "ung ho nguoi ngheo"

    try:
        bin_code = get_bin_code(identifier, bank_list)
        viet_qr.set_beneficiary_organization(bin_code, account_number)
        viet_qr.set_transaction_amount(amount)
        viet_qr.set_additional_data_field_template(purpose)
        qr_data = viet_qr.build()

        bank_name = get_bank_name(bin_code, bank_list)
        print(f"Ngân hàng: {bank_name}")
        print(f"Số tài khoản: {account_number}")
        print(f"Số tiền: {amount} VND")
        print(f"Mục đích: {purpose}")
        print(f"Dữ liệu QR Code: {qr_data}")
        generate_qr_code(qr_data, "vietqr_payment.png")
    except ValueError as e:
        print(f"Lỗi: {e}")