# Hướng dẫn phần giọng nói: thu âm, nhận dạng, đo lường

*Dùng cho mức Standard (tuần 6-9) và Full. Code là khung để bạn chép và chỉnh, chưa chạy thử trên máy bạn; hãy chạy trên vài file trước khi chạy cả bộ.*

## 1. Mục tiêu và thứ được đo

Trả lời RQ1: giọng nói làm tỉ lệ hoàn thành tác vụ giảm bao nhiêu, và biện pháp nào phục hồi được nhiều nhất. Quy trình:

1. Thu âm các câu của khách trong bộ kịch bản (một tập con).
2. Chạy ASR để có văn bản.
3. Đưa văn bản ASR vào cùng agent và cùng script chấm như bản chữ.
4. So sánh với bản chữ chuẩn (V0) để ra voice gap.

Mức Standard chỉ cần chạy trên file ghi âm, không cần thời gian thực.

## 2. Chọn tập con kịch bản để thu âm

Chọn 30 kịch bản chứa nhiều thực thể (mã đơn, số điện thoại, tên sản phẩm, thành phố, số lượng) từ bộ 40 kịch bản:

`01, 02, 03, 04, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 31, 32, 33, 34, 36, 38, 40`

Các kịch bản đổi trả có hai lượt nói (lượt 2 là câu xác nhận), cần thu cả hai file `t1` và `t2`.

## 3. Người đọc và phân công

- 4 người là lý tưởng (tối thiểu 3), có ít nhất hai vùng miền khác nhau, có cả nam và nữ nếu được.
- Mỗi người đọc khoảng 15 kịch bản, xoay vòng để mỗi kịch bản có ít nhất 2 người đọc.
- **Tách theo người nói:** dùng 1-2 người làm tập **dev** (để chỉnh biện pháp giảm lỗi), các người còn lại làm tập **test** và chỉ dùng để báo cáo. Nếu tất cả giọng đều dùng để chỉnh thì kết quả báo cáo bị lạc quan.
- Ghi lại vùng miền tự khai và giới tính để phân tích lỗi, không ghi tên người đọc đi kèm file.

## 4. Mẫu phiếu đồng ý

```
PHIẾU ĐỒNG Ý THAM GIA GHI ÂM

Dự án: Đồ án tốt nghiệp về trợ lý chăm sóc khách hàng có giọng nói tiếng Việt
Người thực hiện: [tên bạn], sinh viên [trường]

Tôi đồng ý đọc một số câu mẫu và cho phép ghi âm giọng nói của tôi.
Mục đích: đánh giá hệ thống nhận dạng giọng nói trong đồ án tốt nghiệp.

Tôi hiểu rằng:
1. Việc tham gia là tự nguyện, tôi có thể dừng bất cứ lúc nào.
2. Bản ghi được gắn mã ẩn danh (ví dụ spk01), không kèm tên tôi.
3. Tôi có thể yêu cầu xóa bản ghi của mình bất cứ lúc nào.
4. Bản ghi chỉ dùng cho mục đích học thuật.
5. Chia sẻ dữ liệu (chọn một):
   [ ] Chỉ dùng nội bộ trong đồ án
   [ ] Được phép công khai cùng bộ dữ liệu (đã ẩn danh)

Vùng miền giọng nói (tùy chọn): ______    Giới tính (tùy chọn): ______
Họ tên: ______________    Ngày: ________    Chữ ký: ____________
```

Lưu phiếu đã ký ở nơi riêng, không đưa lên GitHub. Đây là mẫu tham khảo, nếu trường có quy định về đạo đức nghiên cứu thì hỏi giảng viên hướng dẫn.

## 5. Thiết bị và cách thu

- Micro tai nghe hoặc micro điện thoại đặt cách miệng khoảng 20-30 cm. Dùng cùng một loại thiết bị cho các lần thu của cùng một điều kiện.
- Ba điều kiện: **yên tĩnh** (phòng kín), **ồn nhẹ** (quạt, nhạc nền nhỏ hoặc quán cà phê vắng), **chất lượng điện thoại** (đặt điện thoại xa miệng 30-50 cm). Mỗi người nên đọc ít nhất một nửa số câu ở hai điều kiện.
- Đọc **tự nhiên** như đang nói với tổng đài, không đọc chậm từng chữ. Số điện thoại đọc từng chữ số. Mã đơn đọc “tê en, một không không một”.
- Chuyển định dạng về WAV 16 kHz mono bằng ffmpeg:

```
ffmpeg -i vao.m4a -ar 16000 -ac 1 ra.wav
```

**Quy ước đặt tên:** `spk01_S20_t1_quiet.wav` (người nói, kịch bản, lượt, điều kiện).

## 6. Metadata (data/audio/metadata.csv)

| Cột | Ý nghĩa |
| --- | --- |
| file | Tên file |
| speaker | Mã ẩn danh, ví dụ spk01 |
| region | Bắc, Trung, Nam (tự khai) |
| device | Tai nghe, điện thoại, micro laptop |
| condition | quiet, noisy, phone |
| scenario | Mã kịch bản, ví dụ S20 |
| turn | 1 hoặc 2 |
| split | dev hoặc test (theo người nói) |
| transcript\_gold | Câu đúng người đọc, chép tay sau khi nghe lại |
| gold\_phone, gold\_order, gold\_product | Thực thể đúng (để trống nếu không có) |

Chuẩn định dạng `transcript_gold` theo đúng những gì người đọc đã nói, không chép lại từ kịch bản gốc nếu họ đọc khác đi.

## 7. Kiểm tra chất lượng bộ âm thanh

- Nghe lại ít nhất 20% số file, đặc biệt mỗi người và mỗi điều kiện một vài file.
- Loại file bị cắt tiếng, vỡ tiếng (peak chạm trần), hoặc quá dài bất thường; thu lại thay vì sửa bằng tay.
- Bảng kiểm đủ phủ: mỗi ô (người nói nhân điều kiện) có số file tối thiểu bạn đặt ra trước.
- Tổng thời lượng khoảng vài chục phút là đủ cho đồ án, không cần hàng giờ.

## 8. Tăng dữ liệu bằng nhiễu tổng hợp (ghi rõ trong báo cáo)

```python
import numpy as np
import soundfile as sf

def mix(clean, noise, snr_db):
    # clean, noise: mảng mono float trong [-1, 1]
    if len(noise) < len(clean):
        noise = np.tile(noise, len(clean) // len(noise) + 1)
    noise = noise[:len(clean)]
    pc = np.mean(clean ** 2)
    pn = np.mean(noise ** 2) + 1e-12
    scale = np.sqrt(pc / (pn * 10 ** (snr_db / 10)))
    return np.clip(clean + scale * noise, -1, 1)

clean, sr = sf.read('data/audio/spk01_S20_t1_quiet.wav')
noise, _ = sf.read('data/audio/noise_cafe.wav')
sf.write('data/audio/syn_spk01_S20_t1_snr10.wav', mix(clean, noise, 10), sr)
```

Báo cáo riêng kết quả trên âm thanh tổng hợp, vì nhiễu cộng vào không giống môi trường thật. Chỉ dùng file nhiễu nền bạn có quyền sử dụng.

## 9. Chạy ASR với Faster Whisper

```python
import csv, time, gc
from faster_whisper import WhisperModel

def transcribe_all(model_name, files, out_csv, device='cuda'):
    ctype = 'int8_float16' if device == 'cuda' else 'int8'
    model = WhisperModel(model_name, device=device, compute_type=ctype)
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['file', 'text', 'seconds'])
        for p in files:
            t0 = time.time()
            segs, info = model.transcribe(p, language='vi', beam_size=5, vad_filter=True)
            text = ' '.join(s.text.strip() for s in segs)
            w.writerow([p, text, round(time.time() - t0, 2)])
    del model
    gc.collect()
```

- V1 dùng `small`, V2 dùng `medium` (với RTX 3050 4GB, xem tab Nhánh 3+5 và kiểm tra bằng `nvidia-smi`). Chạy từng model một, giải phóng bộ nhớ trước khi nạp model khác.
- Ghi lại phiên bản thư viện, tên model, `beam_size`, `compute_type`, `vad_filter` vào báo cáo.
- Chạy lại toàn bộ một lần nữa để kiểm tra kết quả ổn định (ASR gần như tất định nhưng hãy kiểm chứng).

## 10. Chuẩn hóa văn bản và thực thể

ASR có thể trả số bằng chữ (“không chín không”) hoặc bằng chữ số, và khác nhau giữa các lần. Các hàm dưới đây đưa về một dạng chung trước khi đưa vào agent (biện pháp M2) và trước khi tính lỗi.

```python
DIGITS = {'không': '0', 'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'tư': '4',
          'năm': '5', 'lăm': '5', 'sáu': '6', 'bảy': '7', 'bẩy': '7', 'tám': '8', 'chín': '9'}

def spoken_digits_to_text(text, min_run=3):
    # chỉ đổi khi có từ 3 từ số liên tiếp trở lên, tránh đổi nhầm “ba”, “năm” trong câu thường
    words = text.lower().replace(',', ' ').replace('.', ' ').split()
    out, run = [], []
    def flush():
        if len(run) >= min_run:
            out.append(''.join(DIGITS[w] for w in run))
        else:
            out.extend(run)
        run.clear()
    for w in words:
        if w in DIGITS:
            run.append(w)
        else:
            flush()
            out.append(w)
    flush()
    return ' '.join(out)

def find_phone(text):
    words = spoken_digits_to_text(text).split()
    run = ''
    for w in words + ['']:
        if w.isdigit():
            run += w
        else:
            if len(run) == 10 and run.startswith('0'):
                return run
            run = ''
    return None

def find_order_id(text):
    t = ''.join(ch if ch.isalnum() else ' ' for ch in spoken_digits_to_text(text))
    words = t.split()
    for i, w in enumerate(words):
        digits = ''
        if w == 'tn' and i + 1 < len(words):
            digits = words[i + 1]
        elif w.startswith('tn') and w[2:].isdigit():
            digits = w[2:]
        elif w in ('tê', 'te') and i + 2 < len(words) and words[i + 1] in ('en', 'nờ'):
            digits = words[i + 2]
        if len(digits) == 4 and digits.isdigit():
            return 'TN-' + digits
    return None
```

**Đối sánh mờ tên sản phẩm (biện pháp M3):**

```python
from rapidfuzz import process, fuzz
from app.agent.confirm import strip_accents

def snap_product(text, catalog_names, cutoff=75):
    best = process.extractOne(strip_accents(text), {n: strip_accents(n) for n in catalog_names}, scorer=fuzz.partial_ratio, score_cutoff=cutoff)
    return best[2] if best else None
```

Nếu có hai sản phẩm gần điểm ngang nhau (ví dụ Nova Buds 2 và Nova Buds Pro), trả cả hai và để agent hỏi lại thay vì chọn đại.

## 11. Đo WER và lỗi thực thể

**WER:** dùng thư viện jiwer. Tiếng Việt viết tách từng âm tiết bằng dấu cách nên WER theo từ gần với tỉ lệ lỗi âm tiết; báo cáo thêm CER để đầy đủ.

```python
import jiwer

def clean(s):
    s = spoken_digits_to_text(s)
    return ' '.join(''.join(ch if ch.isalnum() or ch.isspace() else ' ' for ch in s.lower()).split())

def wer_cer(ref, hyp):
    r, h = clean(ref), clean(hyp)
    return jiwer.wer(r, h), jiwer.cer(r, h)
```

**Tỉ lệ lỗi thực thể:** với mỗi câu có `gold_phone`, `gold_order` hoặc `gold_product`, trích thực thể từ văn bản ASR bằng các hàm trên rồi so sánh. Tỉ lệ lỗi thực thể bằng số thực thể sai chia tổng số thực thể. Báo cáo riêng cho từng loại thực thể vì số điện thoại thường khó hơn tên sản phẩm.

## 12. Chạy agent trên văn bản ASR

Ý tưởng: với mỗi bản ghi, tạo một bản sao của kịch bản mà câu khách là văn bản ASR (có thể qua chuẩn hóa), rồi chạy đúng script eval của bản chữ.

```python
def scenario_from_asr(sc, asr_texts):
    # asr_texts: {1: 'văn bản lượt 1', 2: 'văn bản lượt 2'}
    sc2 = dict(sc)
    sc2['turns'] = [{'user': asr_texts[i + 1]} for i in range(len(sc['turns']))]
    return sc2
```

V0 dùng câu gốc trong kịch bản; V1 đến V4 dùng văn bản ASR tương ứng. Bạn phải so sánh trên **cùng tập kịch bản** và **cùng cấu hình agent**. Kết quả: voice gap cho từng điều kiện bằng tỉ lệ hoàn thành của V0 trừ tỉ lệ hoàn thành ở điều kiện đang xét. Với số mẫu nhỏ (vài chục đến vài trăm lượt), hãy báo cáo số đếm thật (ví dụ 21 trên 30) bên cạnh phần trăm và thừa nhận độ bất định.

## 13. Các biện pháp giảm lỗi (V4)

| Mã | Biện pháp | Cách cài |
| --- | --- | --- |
| M1 | Đọc lại thực thể để khách xác nhận | Thêm vào prompt cho kênh giọng nói: đọc lại mã đơn và số điện thoại từng chữ số và xin xác nhận trước khi gọi công cụ. Đo tỉ lệ agent thực sự làm điều này |
| M2 | Chuẩn hóa số và mã đơn | Áp dụng `spoken_digits_to_text` và `find_*` lên văn bản ASR trước khi đưa cho agent |
| M3 | Đối sánh mờ tên sản phẩm | `snap_product`, hỏi lại khi có nhiều ứng viên gần nhau |
| M4 (tùy chọn) | Đối chiếu hai cấu hình ASR | Nếu small và medium cho thực thể khác nhau thì hỏi lại khách |
| M5 (tùy chọn) | Hỏi bốn số cuối của mã đơn thay vì cả mã | Giảm số thực thể phải nghe đúng, để tiền tố TN do hệ thống tự thêm |

Bật từng biện pháp riêng rồi bật chung để thấy đóng góp của mỗi cái vào voice gap. Chỉ chỉnh tham số (ngưỡng cutoff, quy tắc chuẩn hóa) trên tập âm thanh dev.

## 14. Đo độ trễ (mức Full)

```python
import time

class Marks:
    def __init__(self):
        self.t = {}
    def mark(self, name):
        self.t[name] = time.perf_counter()
    def span(self, a, b):
        return self.t[b] - self.t[a]
```

Đặt các mốc: `t0` hết câu nói, `t1` ASR xong, `t2` token đầu tiên của LLM, `t3` công cụ xong, `t4` văn bản trả lời xong, `t5` âm thanh đầu tiên phát ra. Ghi mỗi lượt thành một dòng nhật ký. Tính p50, p95 theo từng thành phần. Ghi cấu hình máy (GPU, RAM, CPU) và đừng mở ứng dụng nặng khác khi đo.

## 15. Bản demo thời gian thực (mức Full)

Làm theo ba bước tăng dần độ phức tạp, dừng ở bước đủ dùng:

1. **Nhấn giữ để nói:** trình duyệt ghi âm, gửi cả đoạn lên API, nhận văn bản và âm thanh trả lời. Đơn giản và đủ cho demo.
2. **Phát hiện hết câu tự động (VAD)** thay cho nút nhấn giữ.
3. **Streaming** (gửi âm thanh từng đoạn qua WebSocket, phát TTS khi còn đang sinh). Chỉ làm khi bước 1 và 2 đã ổn.

Nếu mất hơn một tuần cho streaming mà chưa ổn, quay về bước 1 và đo độ trễ trên pipeline có mốc thời gian.

## 16. TTS tiếng Việt

- Chọn 1-2 giọng, **kiểm tra điều khoản sử dụng** trước khi dùng cho demo công khai.
- Đánh giá bằng ba thứ: thời gian đến âm thanh đầu tiên, độ tự nhiên (nhờ 3 người chấm 1-5), và **độ rõ khi đọc số** (nhờ người nghe chép lại số điện thoại và mã đơn mà agent đọc, đếm đúng bao nhiêu).
- Khi đọc số điện thoại, đọc từng chữ số và ngắt nhịp theo nhóm, để khách nghe được.

## 17. Danh sách kiểm tra trước khi chốt kết quả

- [ ] Có phiếu đồng ý cho mọi người đọc, lưu ở nơi riêng.
- [ ] Âm thanh đã chuẩn hóa 16 kHz mono, metadata đầy đủ.
- [ ] Ít nhất 20% file đã nghe lại, transcript\_gold đã duyệt.
- [ ] Tách dev và test theo người nói, không chỉnh tham số trên test.
- [ ] Âm thanh tổng hợp được báo cáo riêng.
- [ ] Cấu hình ASR, phiên bản thư viện, thiết bị đã ghi lại.
- [ ] Có bảng WER, lỗi thực thể, voice gap trước và sau biện pháp giảm lỗi.
- [ ] Không đưa âm thanh lên GitHub công khai nếu người đọc chưa đồng ý chia sẻ.
