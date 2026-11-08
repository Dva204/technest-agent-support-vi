# CHÍNH SÁCH BÁN HÀNG VÀ CHĂM SÓC KHÁCH HÀNG TECHNEST

## 1. Chính sách đổi trả sản phẩm

Cửa hàng TechNest hỗ trợ đổi trả sản phẩm cho khách hàng theo các điều kiện sau:

### 1.1. Đổi trả do lỗi kỹ thuật (Nhà sản xuất)
- **Thời hạn áp dụng:** Trong vòng **30 ngày** kể từ ngày khách hàng nhận được sản phẩm (`delivered_at`).
- **Điều kiện:** Sản phẩm phát sinh lỗi kỹ thuật phần cứng do nhà sản xuất (ví dụ: rè loa, lỗi màn hình, không nhận sạc...).
- **Chi phí vận chuyển:** TechNest chịu toàn bộ chi phí vận chuyển phát sinh khi đổi trả hàng lỗi.

### 1.2. Đổi trả do đổi ý (Nhu cầu cá nhân)
- **Thời hạn áp dụng:** Trong vòng **7 ngày** kể từ ngày nhận hàng.
- **Điều kiện bắt buộc:**
  - Sản phẩm phải còn nguyên seal, chưa mở hộp (`opened = 0`).
  - Sản phẩm chưa kích hoạt bảo hành điện tử (`activated = 0`).
- **Ngoại lệ về vệ sinh:** Riêng nhóm sản phẩm **tai nghe nhét tai (earbuds)**, nếu đã mở hộp (`opened = 1`) sẽ **không được đổi trả** vì lý do đổi ý nhằm đảm bảo tiêu chuẩn vệ sinh cá nhân.
- **Sản phẩm đã kích hoạt:** Bất kỳ thiết bị nào đã kích hoạt đều **không được đổi trả vì lý do đổi ý**, chỉ hỗ trợ bảo hành / đổi mới nếu phát sinh lỗi kỹ thuật.
- **Chi phí vận chuyển:** Khách hàng tự thanh toán phí vận chuyển đổi hàng khi đổi vì lý do đổi ý.

### 1.3. Trạng thái đơn hàng không hợp lệ
- Không hỗ trợ đổi trả với các đơn hàng **đã bị hủy** (`cancelled`) hoặc **chưa giao xong** (`shipping`, `processing`).

---

## 2. Quy trình xác nhận đổi trả (Luồng Prepare & Commit)

Để bảo đảm tính minh bạch và tránh thao tác nhầm lẫn, quy trình đổi trả gồm 2 bước:
1. **Kiểm tra điều kiện (Prepare Return):** Hệ thống kiểm tra điều kiện đổi trả theo chính sách. Nếu thỏa mãn, hệ thống cấp mã yêu cầu tạm thời (token) và đưa ra bản tóm tắt xác nhận cho khách hàng.
2. **Xác nhận từ khách hàng (Commit Return):** Trợ lý đọc lại tóm tắt và yêu cầu khách hàng xác nhận rõ ràng. Chỉ khi khách hàng đồng ý xác nhận, yêu cầu đổi trả mới được ghi nhận chính thức vào hệ thống.

---

## 3. Chính sách giao hàng và cước phí vận chuyển

Cước phí giao hàng tiêu chuẩn được áp dụng theo địa chỉ nhận hàng của khách:
- **Nội thành Hà Nội & TP. Hồ Chí Minh:** 20.000 VNĐ.
- **Đà Nẵng:** 30.000 VNĐ.
- **Các tỉnh/thành phố khác:** 40.000 VNĐ.
- **Ưu đãi miễn phí vận chuyển:** Đơn hàng có tổng giá trị tạm tính từ **1.000.000 VNĐ trở lên** được **miễn phí giao hàng toàn quốc**.

---

## 4. Chính sách bảo mật thông tin đơn hàng

- Để tra cứu tiến độ đơn hàng hoặc thực hiện đổi trả, khách hàng **bắt buộc phải cung cấp đúng mã đơn hàng và số điện thoại** trùng khớp với thông tin khi đặt hàng.
- Trợ lý TechNest tuyệt đối **không tiết lộ thông tin đơn hàng** cho bên thứ ba hoặc khi số điện thoại không khớp.
- Nghiêm cấm cung cấp danh sách đơn hàng hoặc dữ liệu của các khách hàng khác.

---

## 5. Chuyển tiếp nhân viên hỗ trợ (Escalation)

Hệ thống sẽ tạo yêu cầu chuyển tiếp sang nhân viên hỗ trợ con người xử lý trong các trường hợp:
- Khách hàng khiếu nại về việc giao thiếu hàng, hàng bị hư hỏng trong quá trình vận chuyển.
- Khách hàng phản ánh thái độ phục vụ chưa tốt của nhân viên.
- Khách hàng chủ động yêu cầu gặp trực tiếp nhân viên hỗ trợ.

---

## 6. Phạm vi hỗ trợ

- Trợ lý TechNest chỉ giải đáp thông tin liên quan đến sản phẩm, đơn hàng, giá bán, bảo hành và chính sách của cửa hàng.
- Lịch sự từ chối các câu hỏi nằm ngoài phạm vi hoạt động của cửa hàng (tài chính, thơ văn, thời sự, lập trình...).
- Nghiêm cấm tự ý đưa ra các ngoại lệ chính sách hoặc bịa đặt thông tin không có trong cơ sở dữ liệu.

