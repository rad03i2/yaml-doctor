# YAML Doctor

A focused command-line tool for validating, diagnosing, formatting, and inspecting YAML files locally.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: [@rad03i2](https://github.com/rad03i2)

## English

### Overview
YAML Doctor helps developers catch YAML problems before configuration reaches CI, deployment, or production. It detects syntax errors and duplicate mapping keys, reports common whitespace problems, formats YAML deterministically, inspects multi-document files, and reads nested values with a simple path syntax.

### Why it exists
YAML parsers can silently accept duplicate keys or configuration that is difficult to review. YAML Doctor deliberately rejects duplicate mapping keys and provides file/line/column diagnostics suitable for local development and CI.

### Features
- Safe YAML parsing through PyYAML `SafeLoader`; YAML content is never executed as Python code.
- Duplicate-key detection with source location.
- Syntax diagnostics with line and column when PyYAML provides them.
- Optional checks for tabs, trailing whitespace, UTF-8 BOM, and configurable line length.
- `--strict` mode that turns warnings into a failing exit code.
- Deterministic formatting, Unicode preservation, optional key sorting, and multi-document support.
- `inspect` command for document count and root types.
- `get` command with paths such as `services[0].name`.
- JSON diagnostic output for automation.
- Reads from stdin with `-`; refuses to overwrite output unless `--force` is explicit.

### Requirements
- Python 3.10+
- PyYAML 6.x

### Installation
```bash
git clone https://github.com/rad03i2/yaml-doctor.git
cd yaml-doctor
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```
For development/testing: `python -m pip install pytest`.

### Usage
```bash
yaml-doctor check config.yml
yaml-doctor check config.yml --strict
yaml-doctor check a.yml b.yml --json
yaml-doctor check - < config.yml
yaml-doctor format config.yml
yaml-doctor format config.yml --sort-keys -o normalized.yml
yaml-doctor inspect compose.yml --json
yaml-doctor get config.yml 'services[0].name'
yaml-doctor --version
```
`check` returns exit code **0** when accepted and **1** when errors exist (or warnings exist under `--strict`). Operational/usage failures return **2**.

### Configuration
YAML Doctor intentionally has no hidden project configuration. Checks are explicit CLI options: `--max-line-length N`, `--allow-tabs`, and `--strict`. This keeps CI behavior visible and reproducible.

### Preview guidance
For a repository screenshot, run `yaml-doctor check examples/sample.yml` and `yaml-doctor inspect examples/sample.yml --json` in a clean terminal. No screenshot is committed because terminal rendering depends on the user's platform/theme.

### Project structure
```text
src/yaml_doctor/core.py   parsing, diagnostics, formatting, queries
src/yaml_doctor/cli.py    CLI and exit-code behavior
tests/                    functional and CLI tests
examples/sample.yml       safe sample input
.github/workflows/ci.yml  cross-platform tests
```

### Testing
```bash
python -m pip install -e . pytest
python -m pytest
```
CI runs the same suite on Python 3.10, 3.12, and 3.13 across Ubuntu, Windows, and macOS.

### Security & privacy
All processing is local. There is no telemetry, network request, account, token, or API key. YAML is loaded with a SafeLoader-derived loader. Output files are not overwritten without `--force`. Treat untrusted files as data and review formatted output before replacing production configuration.

### Limitations
YAML Doctor is not a full style linter, schema validator, YAML Language Server, or editor plugin. `get` implements a deliberately small dotted/index path syntax, not JSONPath/JMESPath. Formatting may change comments because PyYAML does not preserve comments. YAML aliases supported by PyYAML are supported, but round-trip presentation details are not preserved.

### Optional roadmap
Possible future additions include JSON Schema validation, comment-preserving round trips, and configurable policy files. These are not claimed as current features.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports should include a minimal non-sensitive YAML sample and expected behavior.

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**

---

## العربية

### نظرة عامة
YAML Doctor أداة سطر أوامر محلية للتحقق من ملفات YAML وتشخيص أخطائها وتنسيقها وفحص بنيتها قبل استخدامها في CI أو النشر أو بيئات الإنتاج. تكشف أخطاء الصياغة والمفاتيح المكررة ومشكلات المسافات الشائعة، وتدعم الملفات متعددة المستندات وقراءة القيم المتداخلة.

### لماذا هذا المشروع؟
قد تقبل بعض محللات YAML مفاتيح مكررة بصمت، مما يجعل الإعداد النهائي مختلفًا عما يتوقعه المطور. لذلك يرفض YAML Doctor المفاتيح المكررة صراحة ويعرض موضع المشكلة قدر الإمكان.

### المميزات
- تحليل آمن مبني على `SafeLoader` دون تنفيذ محتوى YAML ككود Python.
- كشف المفاتيح المكررة مع رقم السطر والعمود.
- تشخيص أخطاء الصياغة، وعلامات التبويب، والمسافات النهائية، وBOM، وطول السطر.
- وضع `--strict` لجعل التحذيرات سببًا لفشل الفحص.
- تنسيق موحد مع دعم Unicode والعربية وترتيب المفاتيح اختياريًا.
- دعم YAML متعدد المستندات.
- أمر `inspect` لمعرفة عدد المستندات وأنواع الجذور.
- أمر `get` لمسارات مثل `services[0].name`.
- إخراج JSON مناسب للأتمتة وCI.
- القراءة من stdin ومنع استبدال ملف إخراج موجود دون `--force`.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث وPyYAML 6.x.
```bash
git clone https://github.com/rad03i2/yaml-doctor.git
cd yaml-doctor
python -m venv .venv
python -m pip install -e .
```

### أمثلة الاستخدام
```bash
yaml-doctor check config.yml
yaml-doctor check config.yml --strict
yaml-doctor check config.yml --json
yaml-doctor format config.yml --sort-keys -o normalized.yml
yaml-doctor inspect config.yml --json
yaml-doctor get config.yml 'services[0].name'
```
يعيد `check` الرمز 0 عند نجاح الفحص، والرمز 1 عند وجود أخطاء أو تحذيرات في الوضع الصارم، والرمز 2 للأخطاء التشغيلية أو أخطاء الاستخدام.

### الإعداد
لا توجد إعدادات مخفية أو متغيرات بيئة مطلوبة. يمكن التحكم مباشرة بخيارات `--max-line-length` و`--allow-tabs` و`--strict`.

### بنية المشروع والاختبارات
المنطق الأساسي داخل `src/yaml_doctor/core.py`، وواجهة الأوامر داخل `cli.py`، والاختبارات داخل `tests/`، ويوجد مثال آمن داخل `examples/`. لتشغيل الاختبارات:
```bash
python -m pip install -e . pytest
python -m pytest
```
ويشغّل CI الاختبارات على أنظمة Ubuntu وWindows وmacOS وإصدارات Python المحددة في workflow.

### إرشادات المعاينة
لإنشاء صورة معاينة للمستودع شغّل `yaml-doctor check examples/sample.yml` ثم `yaml-doctor inspect examples/sample.yml --json` في نافذة طرفية نظيفة. لم نضع لقطة ثابتة لأن مظهر الطرفية يختلف حسب النظام والثيم.

### الخصوصية والأمان
تتم المعالجة محليًا بالكامل ولا توجد Telemetry أو اتصالات شبكة أو حسابات أو مفاتيح API. يستخدم المشروع محلل YAML آمنًا، ولا يستبدل ملفات الإخراج الموجودة إلا عند طلب `--force` صراحة.

### القيود
المشروع ليس مدقق أنماط شاملًا ولا مدقق JSON Schema ولا Language Server. صيغة المسار في `get` مبسطة وليست JSONPath أو JMESPath. كما أن PyYAML لا يحافظ على التعليقات وتفاصيل العرض عند إعادة التنسيق.

### تطوير اختياري مستقبلًا
يمكن مستقبلًا إضافة JSON Schema وتنسيق يحافظ على التعليقات وسياسات قابلة للتهيئة، لكنها ليست ميزات حالية.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة و[SECURITY.md](SECURITY.md) للأمان. المشروع مرخص بترخيص MIT الموضح في [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**
