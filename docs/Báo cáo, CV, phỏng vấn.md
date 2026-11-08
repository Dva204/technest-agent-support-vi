# Hướng dẫn báo cáo, README, CV và phỏng vấn

*Biến kết quả kỹ thuật thành thứ hội đồng chấm được và nhà tuyển dụng đọc được. Các mẫu dưới đây dùng dấu \[điền số thật\] để bạn tự điền từ các lần chạy của mình.*

## 1. Nguyên tắc trung thực

- **Mọi con số trong báo cáo, README, CV phải lấy từ file kết quả đã lưu** trong `experiments/`, kèm ngày chạy, tên model, phiên bản, cấu hình. Không điền số ước lượng hay số “có vẻ hợp lý”.
- Ghi rõ dữ liệu là **giả lập**, không có khách hàng thật, bộ kịch bản do một người viết.
- Nói rõ phần nào là của bạn, phần nào dùng công cụ có sẵn, và nếu dùng trợ lý AI để viết code thì bạn phải hiểu và giải thích được mọi đoạn quan trọng.
- Không nêu tài liệu tham khảo mà bạn chưa đọc. Danh mục tài liệu tự bạn tìm và kiểm tra; mình không dựng sẵn danh sách vì không thể bảo đảm đúng từng trích dẫn.
- Nếu dùng chung phần nào với môn học hoặc đồ án khác, ghi rõ và hỏi giảng viên.

## 2. Cấu trúc báo cáo đồ án

| Chương | Nội dung | Gợi ý | Hình, bảng nên có |
| --- | --- | --- | --- |
| 1. Mở đầu | Động lực, mục tiêu, câu hỏi nghiên cứu RQ0-RQ2, phạm vi, đóng góp | 3-4 trang | Sơ đồ tổng quan |
| 2. Cơ sở lý thuyết và công trình liên quan | LLM gọi công cụ, agent, nhận dạng giọng nói, tổng hợp giọng nói, cách đánh giá agent và độ đo WER | 6-8 trang | Bảng so sánh các hướng tiếp cận |
| 3. Thiết kế hệ thống | Kiến trúc, công cụ, luồng xác nhận, chính sách, CSDL, pipeline giọng nói | 8-10 trang | Sơ đồ kiến trúc, sơ đồ trạng thái luồng xác nhận, bảng công cụ |
| 4. Dữ liệu và phương pháp đánh giá | Kịch bản, chấm theo trạng thái cuối, dev/test, thu âm, đạo đức dữ liệu | 6-8 trang | Bảng phân bố kịch bản, bảng độ phủ người nói nhân điều kiện |
| 5. Thí nghiệm và kết quả | Bảng 1-3 (agent, voice gap, độ trễ), chi phí, độ dao động | 8-12 trang | Biểu đồ voice gap, chất lượng so với độ trễ và chi phí |
| 6. Phân tích lỗi và thảo luận | Phân loại lỗi, ví dụ cụ thể, vì sao biện pháp có hiệu quả hoặc không | 5-6 trang | Bảng lỗi (xem mục 4) |
| 7. Hạn chế | Dữ liệu giả lập, mẫu nhỏ, phụ thuộc mô hình, chưa có người dùng thật | 2-3 trang |  |
| 8. Kết luận và hướng phát triển | Trả lời từng RQ, việc tiếp theo | 2 trang |  |
| Phụ lục | Prompt hệ thống, schema công cụ, danh sách kịch bản, mẫu phiếu đồng ý (không có chữ ký) |  |  |

Số trang chỉ là gợi ý, hãy theo quy định của khoa. Chương 4 và 5 là nơi hội đồng đọc kỹ nhất.

**Trả lời từng RQ ở chương kết luận bằng một đoạn ngắn có số:**

- RQ0: xác nhận và quy tắc chính sách làm hành động sai thay đổi từ \[A1\] sang \[A2\] trên tập test.
- RQ1: voice gap ở điều kiện \[V3\] là \[x\], còn \[y\] sau biện pháp \[M?\].
- RQ2: thành phần chiếm nhiều độ trễ nhất là \[?\], p95 tổng là \[x\] giây trên máy \[cấu hình\].

## 3. Đe dọa tới tính hợp lệ (mục nên có trong chương 7)

- Khách hàng và dữ liệu là giả lập; hành vi người dùng thật có thể khác.
- Bộ kịch bản do một người viết nên có thể thiên lệch theo cách diễn đạt của bạn.
- Số người nói và số câu ít nên kết quả âm thanh có độ bất định lớn.
- Kết quả phụ thuộc phiên bản model tại thời điểm chạy.
- Nếu dùng LLM làm giám khảo thì có thể lệch so với người; ghi số mẫu đã đối chiếu bằng tay.
- Bộ nhận diện xác nhận dựa trên luật, có thể bỏ sót cách nói xác nhận khác.

## 4. Phân tích lỗi

**Phân loại lỗi gợi ý:**

| Mã | Loại lỗi | Ví dụ |
| --- | --- | --- |
| E1 | Chọn sai công cụ | Dùng search\_products thay vì check\_stock để trả lời tồn kho |
| E2 | Sai tham số | Nhầm mã đơn, đảo số điện thoại |
| E3 | Bỏ qua xác nhận | Gọi commit\_return khi khách chưa đồng ý (ở A1) |
| E4 | Vi phạm chính sách | Đồng ý đổi quá hạn khi khách nói “ngoại lệ” |
| E5 | Lộ thông tin | Nêu trạng thái đơn của người khác |
| E6 | Bịa thông tin | Đưa ra giá hoặc ngày về hàng không có trong dữ liệu |
| E7 | Vòng lặp hoặc bỏ dở | Không kết thúc hội thoại, hết số bước |
| E8 | Lỗi do ASR | Nghe nhầm mã đơn dẫn đến tra sai đơn |
| E9 | Từ chối thừa | Từ chối một yêu cầu hợp lệ |

**Bảng ghi lỗi trong báo cáo (mỗi lỗi một dòng):**

| Kịch bản | Cấu hình | Loại | Chuyện gì xảy ra | Nguyên nhân | Đã sửa chưa và cách sửa | Bài học |
| --- | --- | --- | --- | --- | --- | --- |
| \[S?\] | \[A?\] | \[E?\] | \[mô tả ngắn\] | \[nguyên nhân\] | \[có/không\] | \[một câu\] |

Chọn 5-8 lỗi đại diện để phân tích sâu trong chương 6, phần còn lại để ở phụ lục. Đếm số lỗi theo loại để thấy loại nào nhiều nhất ở từng cấu hình.

## 5. Mẫu README

```
# TechNest Agent: trợ lý chăm sóc khách hàng có đo lường

Một dòng mô tả: agent gọi công cụ trên cửa hàng giả lập, có bộ kịch bản chấm theo trạng thái cuối.
[Ảnh hoặc GIF demo: khung chat và bảng soi bên trong]

## Bài toán
Ai dùng, làm gì, vì sao khó (2-3 câu).

## Kết quả chính
Bảng các cấu hình A0, A1, A2 trên tập test: [điền số thật] hoàn thành tác vụ, [điền số thật] hành động sai, [điền số thật] chi phí mỗi hội thoại.
Model, phiên bản, ngày chạy, số lần chạy lặp.

## Kiến trúc
Sơ đồ một hình và một đoạn giải thích luồng prepare và commit.

## Cách đo
Trạng thái cuối của CSDL, 40 kịch bản (25 dev, 15 test), nguyên tắc không chỉnh trên test.

## Quyết định thiết kế
3-5 dòng: chọn gì, vì sao, đã thử gì khác.

## Hạn chế
Dữ liệu giả lập, mẫu nhỏ, phụ thuộc phiên bản model.

## Chạy thử
git clone, copy .env.example thành .env, docker compose up, python -m eval.run A2 dev

## Cấu trúc thư mục
Một đoạn ngắn.
```

Thêm file `.env.example` (không có key thật) và đặt `.env` trong `.gitignore`. Tự chạy các lệnh trên một thư mục mới trước khi nộp.

## 6. Slide bảo vệ (khoảng 12 slide, 15-20 phút)

| Slide | Nội dung | Thời gian |
| --- | --- | --- |
| 1 | Tên đề tài, một câu nói dự án làm gì | 0,5 phút |
| 2 | Vấn đề và vì sao khó (agent làm sai hành động, giọng nói dễ nghe nhầm) | 1,5 phút |
| 3 | Câu hỏi nghiên cứu | 1 phút |
| 4 | Kiến trúc hệ thống | 2 phút |
| 5 | Luồng xác nhận và việc tách prepare, commit | 1,5 phút |
| 6 | Cách đo: trạng thái cuối, bộ kịch bản, dev và test | 2 phút |
| 7 | Kết quả agent (A0, A1, A2) | 2 phút |
| 8 | Thu âm và voice gap | 2 phút |
| 9 | Biện pháp giảm lỗi và hiệu quả | 1,5 phút |
| 10 | Độ trễ và chi phí | 1,5 phút |
| 11 | Demo trực tiếp (có video dự phòng) và hai lỗi thật | 2 phút |
| 12 | Hạn chế và hướng phát triển | 1 phút |

Mỗi slide chỉ một ý, ưu tiên biểu đồ hơn chữ. Chuẩn bị video demo ngắn trong máy đề phòng khi mạng hoặc API lỗi.

## 7. Mô tả dự án trên CV (khung để điền)

**Tiêu đề:** TechNest Agent, trợ lý chăm sóc khách hàng có tool-calling và giao diện giọng nói tiếng Việt (link GitHub, link demo)

- Xây dựng agent gọi \[số\] công cụ trên cửa hàng giả lập bằng Python, FastAPI, Docker; tách thao tác ghi dữ liệu thành prepare và commit có bước xác nhận được ứng dụng ép buộc.
- Thiết kế bộ \[số\] kịch bản chấm theo trạng thái cuối của CSDL (tách dev và test); hành động sai giảm từ \[số\]% xuống \[số\]% so với baseline.
- Tích hợp nhận dạng giọng nói (Faster Whisper) và đo tác động của lỗi nhận dạng lên tỉ lệ hoàn thành tác vụ: giảm \[số\] điểm phần trăm trên \[số\] bản ghi, phục hồi \[số\] điểm nhờ chuẩn hóa số và xác nhận thực thể.
- Đo độ trễ theo thành phần và chi phí mỗi hội thoại: p95 \[số\] giây, \[số\] đồng mỗi hội thoại.

Chỉ viết những dòng mà bạn đã làm và có số để chứng minh. Nếu mức Lite là mức cao nhất bạn đã làm khi nộp hồ sơ, bỏ dòng về giọng nói và ghi “đang phát triển phần giọng nói”. Khi nộp, dùng các từ khóa trong mô tả công việc mà bạn thật sự đã làm (RAG, tool-calling, FastAPI, Docker, đánh giá). Không liệt kê kỹ năng chưa dùng.

## 8. GitHub và bản demo

- Ghim repo này lên hồ sơ; đặt mô tả ngắn và các topic (agent, tool-calling, speech-recognition, vietnamese).
- README có ảnh hoặc GIF demo ở đầu, bảng kết quả ở nửa trên.
- Thêm giới hạn số lượt gọi cho bản demo công khai và ẩn API key.
- Có file LICENSE, và ghi rõ dữ liệu là giả lập.
- Không để lịch sử commit chứa key hay dữ liệu ghi âm chưa được phép.

## 9. Kịch bản trình bày 3 phút cho phỏng vấn

1. **Vấn đề (20 giây):** “Chatbot chăm sóc khách hàng không chỉ trả lời mà còn thực hiện hành động như tạo yêu cầu đổi trả. Sai một lần là gây hậu quả thật, và với giọng nói thì còn dễ nghe nhầm mã đơn.”
2. **Giải pháp (40 giây):** vẽ sơ đồ một hình; nhấn mạnh prepare và commit và việc ứng dụng, không phải prompt, chặn hành động khi chưa có xác nhận.
3. **Cách đo (40 giây):** chấm theo trạng thái cuối CSDL, 40 kịch bản tách dev và test, chạy lặp.
4. **Kết quả đáng nhớ (40 giây):** một con số thật, ví dụ hành động sai giữa A1 và A2 hoặc voice gap trước và sau.
5. **Một lỗi thật (30 giây):** một lỗi bạn gặp, nguyên nhân, cách sửa, bài học.
6. **Tiếp theo (10 giây):** một việc bạn sẽ làm nếu có thêm thời gian.

## 10. Bộ câu hỏi phỏng vấn và ý chính trả lời

**Về agent và công cụ**

| Câu hỏi | Ý chính |
| --- | --- |
| Vì sao tách prepare và commit? | Để ứng dụng chặn được hành động ghi dữ liệu khi chưa có xác nhận; phụ thuộc prompt thì không đảm bảo và không đo được |
| Sao không dùng LangChain hay framework agent? | Tự viết vòng lặp vài chục dòng để hiểu và kiểm soát; sẽ dùng framework khi cần tính năng mà việc tự viết không đáng |
| Nếu mô hình gọi sai công cụ thì sao? | Công cụ trả mã lỗi có cấu trúc, giới hạn số bước, quy tắc chính sách ở tầng ứng dụng, có số liệu lỗi |
| Làm sao chống chèn lệnh? | Không tin vào prompt; quyền truy cập dữ liệu kiểm ở tầng công cụ (số điện thoại phải khớp đơn), có kịch bản thử đo tỉ lệ kháng cự |

**Về đánh giá**

| Câu hỏi | Ý chính |
| --- | --- |
| Làm sao biết kết quả đáng tin? | Tách dev và test, chạy test một lần, chạy lặp cấu hình chính, báo cáo số đếm thật và độ dao động |
| 40 kịch bản có đủ không? | Đủ để thấy xu hướng và bắt lỗi, không đủ để kết luận thống kê chắc chắn; thừa nhận và nêu hướng mở rộng |
| Sao chấm theo trạng thái cuối? | Không phụ thuộc cách diễn đạt, phản ánh hành động thật của hệ thống |
| Kết quả có thay đổi nếu đổi model không? | Có thể; đã ghi phiên bản và làm lớp bọc để chạy lại dễ dàng |

**Về giọng nói**

| Câu hỏi | Ý chính |
| --- | --- |
| Giọng nói làm tệ đi bao nhiêu? | Nêu voice gap và loại thực thể gây lỗi nhiều nhất |
| Nghe nhầm số điện thoại thì sao? | Chuẩn hóa số, đọc lại để xác nhận, có số liệu trước và sau |
| Vì sao chọn model ASR này? | So sánh small và medium, nêu đánh đổi độ chính xác và độ trễ trên phần cứng của bạn |
| Người nói ít có sao không? | Thừa nhận, tách dev và test theo người nói, báo cáo âm thanh tổng hợp riêng |

**Về thực tế triển khai và sản phẩm**

| Câu hỏi | Ý chính |
| --- | --- |
| Muốn triển khai thật cần thêm gì? | Xác thực khách thật, giới hạn tốc độ, theo dõi và đánh giá liên tục, bảo vệ dữ liệu cá nhân, luồng chuyển người thật |
| Dự án có người dùng thật không? | Không; đây là nghiên cứu có kiểm soát trên dữ liệu giả lập, nêu rõ điều này là hạn chế |
| Chi phí thế nào? | Bảng token và chi phí mỗi hội thoại theo cấu hình |
| Em dùng AI để viết code đúng không? | Trả lời thẳng nếu có; nhấn mạnh em đọc, hiểu, kiểm thử và giải thích được từng phần quan trọng |
| Lỗi lớn nhất em gặp? | Chọn một lỗi thật trong bảng lỗi, nói nguyên nhân và cách sửa |
| Nếu có thêm thời gian thì làm gì? | Một việc cụ thể trong phần hạn chế (ví dụ thêm người nói, thêm kịch bản khó) |

Không cần học thuộc lòng. Hãy luyện trả lời bằng chính số liệu và ví dụ trong dự án của bạn.

## 11. Kế hoạch một tuần trước phỏng vấn

| Ngày | Việc |
| --- | --- |
| 1 | Đọc lại toàn bộ code, chạy lại repo trên thư mục mới |
| 2 | Viết bản trình bày 3 phút và 10 phút, tập nói to |
| 3 | Chuẩn bị hai lỗi thật và cách sửa, tập vẽ sơ đồ kiến trúc trên giấy |
| 4 | Tập trả lời các câu hỏi ở mục 10, nhờ bạn hỏi ngẫu nhiên |
| 5 | Làm video demo dự phòng, kiểm tra mạng và API key |
| 6 | Ôn lại con số chính trong bảng kết quả |
| 7 | Nghỉ ngơi, kiểm tra CV và link |

## 12. Bài blog kỹ thuật ngắn (1 trang)

Đề tài gợi ý: **“Đo agent bằng trạng thái cuối của CSDL: bài học từ dự án chatbot chăm sóc khách hàng”**. Dàn ý: vấn đề (chấm câu trả lời không đủ), cách làm (reset dữ liệu, so trạng thái), một ví dụ cụ thể, một con số thật, hạn chế. Link bài vào README và CV.

## 13. Danh sách kiểm tra trước khi nộp hồ sơ và báo cáo

- [ ] Mọi con số đều lấy từ file kết quả, có ngày và cấu hình.
- [ ] README có bảng kết quả, hạn chế và lệnh chạy đã tự thử trên thư mục mới.
- [ ] Không có key hay dữ liệu âm thanh chưa được phép trong repo (kể cả lịch sử commit).
- [ ] Đã nói rõ dữ liệu giả lập và phần dùng chung với môn khác (nếu có).
- [ ] Bảng lỗi có ít nhất 5 dòng và đã chọn một lỗi để kể khi phỏng vấn.
- [ ] CV chỉ có những dòng bạn đã làm và giải thích được.
- [ ] Có video demo dự phòng.
- [ ] Đã xin ý kiến giảng viên về đề cương và việc thu âm người thật.
