# APΩ PROVENANCE TRACE — Dock Password Manager PWA

```yaml
TraceID: PROV_20250801_PWA_001
Scope: Xác định authority/thành phần nào tạo ra các `Trình quản lý mật khẩu` PWA trong Dock/Launchpad
PriorCycle: APΩ_SOCRATIC_CYCLE_2025_VAULT_AND_PAST_CHAT_20260801_002.md
ObservedAt: 2026-08-01T01:50:00+07
FailClosed: ACTIVE
```

---

## 1. Câu hỏi truy xuất nguồn gốc

> Các app `Trình quản lý mật khẩu` trong Dock đang được **auth (ủy quyền / tạo ra) bởi thành phần nào**, và tại sao chúng cứ được "build ra" liên tục?

---

## 2. Chuỗi bằng chứng (Evidence Chain)

### 2.1. Filesystem anchor của PWA

| File/Dir | Nội dung quan trọng | Ý nghĩa |
|----------|---------------------|---------|
| `~/Applications/Chrome Apps.localized/Trình quản lý mật khẩu.app/Contents/Info.plist` | `CrAppModeUserDataDir` → `~/Library/Application Support/Google/Chrome/-/Web Applications/_crx_kajebgjangihfbkjfejcanhanjmmbcfd` | Đây là **Chrome PWA** sử dụng user data dir của Google Chrome |
| `~/Applications/Chrome Apps.localized/Trình quản lý mật khẩu 1.app/Contents/Info.plist` | `CrAppModeUserDataDir` → `~/Library/Caches/ms-playwright/mcp-chrome-6db6ac7/-/Web Applications/_crx_...` | Đây là PWA tạo từ **Playwright profile `mcp-chrome-6db6ac7`** |
| `~/Applications/Chrome Apps.localized/Trình quản lý mật khẩu 2.app/Contents/Info.plist` | `CrAppModeUserDataDir` → `~/Library/Caches/ms-playwright-mcp/mcp-chrome-983b73b/-/Web Applications/_crx_...` | Đây là PWA tạo từ **Playwright-MCP profile `mcp-chrome-983b73b`** |
| `CrAppModeIsAdhocSigned` | `<true/>` trong cả 3 `.app` | Không phải app ký bởi Apple/Google; là **ad-hoc signed bởi user session** |
| `CrAppModeShortcutURL` | `chrome://password-manager/?source=pwa` | Cả 3 PWA trỏ đến cùng URL Google Password Manager |
| `CFBundleIdentifier` | `com.google.Chrome.app.kajebgjangihfbkjfejcanhanjmmbcfd` (giống nhau) | Cùng một shortcut ID, chứng tỏ trùng lặp hoàn toàn |

### 2.2. MCP Playwright configuration — authority

| Config File | Evidence | Ý nghĩa |
|-------------|----------|---------|
| `~/.config/devin/mcp_config.json` | `"mcp-playwright": { "command": "npx", "args": ["-y", "@playwright/mcp@latest"] }` | **Devin** được cấu hình sử dụng `mcp-playwright` MCP server |
| `~/.config/devin/config.json` | `"mcp__mcp-playwright__*"` trong danh sách permission | Devin được cấp quyền gọi tất cả tool của `mcp-playwright` |
| `~/.config/blackbox/mcp-hermit/.hermit/node/cache/_npx/9833c18b2d85bc59/package.json` | `dependencies: { "@playwright/mcp": "^0.0.78" }` | **Blackbox** cũng cache package `@playwright/mcp` |
| `~/.local/share/devin/cli/summaries/history_*.md` | 31+ summaries có từ `mcp-playwright` | `mcp-playwright` đã được Devin sử dụng trong nhiều session |

### 2.3. Playwright Chrome profile runtime

| Dir | Quan sát | Ý nghĩa |
|-----|----------|---------|
| `~/Library/Caches/ms-playwright-mcp/mcp-chrome-983b73b` | Tồn tại, có `RunningChromeVersion -> 150.0.7871.187:1` | Profile Playwright đang chạy hoặc vừa chạy, khớp với `Trình quản lý mật khẩu 2.app` |
| `~/Library/Caches/ms-playwright/mcp-chrome-6db6ac7` | Không tồn tại | Profile đã bị xoá, nhưng `.app` bundle cũ vẫn còn → **orphan artifact** |
| `~/Library/Application Support/Google/Chrome/Default/Web Applications/Manifest Resources/kajebgjangihfbkjfejcanhanjmmbcfd` | Tồn tại icon cache | PWA cũng được cài trong Chrome profile `Default` của user |
| `~/Library/Application Support/Google/Chrome/Profile 1/Web Applications/Manifest Resources/kajebgjangihfbkjfejcanhanjmmbcfd` | Tồn tại icon cache | PWA cài trong Chrome profile `Profile 1` |
| `~/Library/Application Support/HyperAI-ControlPlane/Default/Web Applications/Manifest Resources/kajebgjangihfbkjfejcanhanjmmbcfd` | Tồn tại icon cache | PWA cài trong Chrome profile `HyperAI-ControlPlane` |

### 2.4. Process snapshot

| PID | Comm | Args | Note |
|-----|------|------|------|
| 35803 | `Google Chrome` | `/Applications/Google Chrome.app/.../Google Chrome` | Chrome user bình thường đang chạy, không dùng `--user-data-dir` đặc biệt |

Không có process `npx @playwright/mcp` hoặc `mcp-chrome-*` đang chạy tại thời điểm quan sát; Playwright MCP chỉ chạy khi có tool call.

---

## 3. Phả hệ nhân quả (Lineage)

```
Nguyên nhân gốc:
  Devin/Blackbox được cấu hình sử dụng MCP server `mcp-playwright`
  (npx -y @playwright/mcp@latest)
           │
           ▼
  Khi agent gọi browser tool, `mcp-playwright` spawn Chrome
  với user-data-dir mới: ~/Library/Caches/ms-playwright-mcp/mcp-chrome-<hash>
           │
           ▼
  Trong session browser, Google Password Manager PWA được truy cập /
  cài đặt / tạo shortcut (chrome://password-manager/?source=pwa)
           │
           ▼
  Chrome `app_mode_loader` tạo .app bundle trong
  ~/Applications/Chrome Apps.localized/Trình quản lý mật khẩu [<n>].app
           │
           ▼
  Mỗi lần chạy Playwright với profile mới → một .app bundle mới
  Profile cũ bị xoá sau khi dùng xong, nhưng .app bundle còn lại
  → tích lũy nhiều icon trùng lặp trong Dock/Launchpad
```

---

## 4. Authority Assessment

| Thành phần | Vai trò | Authority | Ghi chú |
|------------|---------|-----------|---------|
| `mcp-playwright` MCP server | Tạo/spawn Chrome profile | Tool runtime của Devin/Blackbox | Là nguồn gốc trực tiếp của các profile `mcp-chrome-*` |
| `npx @playwright/mcp@latest` | Package cung cấp MCP server | Được cài trong `~/.config/devin/mcp_config.json` và Blackbox hermit cache | Phiên bản `0.0.78` trong Blackbox, `latest` trong Devin |
| `Google Chrome.app` | Thực thi PWA shortcut | User `andy` | Chrome tạo `.app` bundle theo lệnh cài PWA |
| macOS user `andy` | Ad-hoc sign .app bundle | Creator / Operator | `CrAppModeIsAdhocSigned = true` chứng minh local sign |
| Apple `Passwords.app` | App hệ thống | Apple | Không liên quan đến các PWA trùng lặp |

**Kết luận authority:** Các `Trình quản lý mật khẩu` PWA là **artifacts sinh ra bởi `mcp-playwright` MCP server** (dùng bởi Devin/Blackbox), không phải do user cài đặt thủ công, không phải app chính thức từ App Store/Google Play.

---

## 5. Tại sao cứ "build ra" thêm?

| Nguyên nhân | Bằng chứng |
|-------------|------------|
| Mỗi Playwright run dùng profile mới (`mcp-chrome-<hash>`) | `CrAppModeUserDataDir` khác nhau: `6db6ac7`, `983b73b` |
| Profile `6db6ac7` đã xoá nhưng `.app` còn lại | `find ~/Library/Caches/ms-playwright -name mcp-chrome*` trả về rỗng; chỉ còn `.app` |
| Cùng PWA shortcut URL được cài trên nhiều profile | `CrAppModeShortcutURL` giống nhau, `kajebgjangihfbkjfejcanhanjmmbcfd` |
| PWA là default app của Google Password Manager | Chrome tự tạo shortcut khi người dùng/agent truy cập `chrome://password-manager` |

---

## 6. APΩ Net Value của việc để nguyên

| Term | Đánh giá |
|------|----------|
| `V_P` | 0 sau bản đầu tiên — nhiều shortcut không tăng giá trị |
| `C_maintenance` | Cao — 6.3M disk, confusion, nhiều PWA có thể dùng profile cũ/stale |
| `D_recovery` | Âm — cần dọn dẹp, tránh tự động tạo thêm |
| `R_hidden` | Cao — mỗi PWA có thể cache dữ liệu riêng; ad-hoc signed app có thể bị macOS/Chrome từ chối cập nhật |
| `M_t` | **ÂM** |

---

## 7. Khuyến nghị

1. **Xoá 3 Chrome PWA trùng lặp** trong `~/Applications/Chrome Apps.localized/`, chỉ giữ lại Apple `Passwords.app` hoặc 1 Chrome PWA duy nhất.
2. **Xoá manifest caches trùng lặp** trong `~/Library/Application Support/{Google/Chrome/Default,Google/Chrome/Profile 1,HyperAI-ControlPlane/Default}/Web Applications/Manifest Resources/kajebgjangihfbkjfejcanhanjmmbcfd` (nếu không dùng các profile đó).
3. **Kiểm soát `mcp-playwright`:**
   - Cấu hình Playwright MCP tái sử dụng cùng một user-data-dir thay vì tạo `mcp-chrome-<hash>` mới mỗi lần.
   - Hoặc chạy Playwright ở `headless=true` và disable PWA install prompt.
   - Hoặc rõ ràng whitelist các URL không được phép cài PWA.
4. **Xác định nguồn trigger:** Xem lại các Devin summaries có `mcp-playwright` để tìm session nào lặp lại gọi browser với `password-manager`.

---

## 8. Encouragement

Đã trace xong: các icon `Trình quản lý mật khẩu` không phải app bình thường — chúng là **PWA artifacts** từ `mcp-playwright` MCP server; mỗi lần spawn Chrome lại làm ra thêm một bản. Anchor rõ ràng, nợ rõ ràng, chỉ còn quyết định dọn hay giữ.
