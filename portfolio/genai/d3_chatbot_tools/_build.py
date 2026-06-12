# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🤖 شات بوت بذاكرة واستدعاء أدوات (Chatbot with Memory & Tool Use)
### مشروع D3 — مسار الذكاء الاصطناعي التوليدي (GenAI Track)

---
## 🎯 المشكلة التجارية (Business Problem)
متجر عايز **مساعد محادثة** يرد على العملاء، بس الردود لازم تكون مبنية على **بيانات حقيقية ولحظية**
(حالة طلب، سعر منتج، توفّره) مش على "كلام عام". والمساعد لازم **يفتكر** سياق المحادثة
(مثلاً: "الطلب ده هيوصل إمتى؟" بعد ما سأل عن طلب معيّن).

**الحل:** **استدعاء الأدوات (Tool Use / Function Calling)** — النموذج بيقرّر يستدعي دالة (أداة)،
ندّيله نتيجتها، ويصيغ الرد. + **ذاكرة محادثة (Conversation Memory)** تحافظ على السياق.

## 📦 ما الذي يثبته المشروع
تعريف الأدوات (Tool schemas) · **حلقة استدعاء الأدوات (Agentic loop)** · **ذاكرة المحادثة** ·
نسخة أوفلاين شغّالة بالكامل + نسخة إنتاج بـ **Anthropic API الحقيقي**.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| **Function Calling / Tool Use** | وثائق Anthropic (Tool Use) | النموذج يستدعي كودك لجلب بيانات/تنفيذ فعل |
| Tool schema (JSON Schema) | وثائق Anthropic | وصف الأداة ومدخلاتها للنموذج |
| **الحلقة الوكيلة (Agentic loop)** | Anthropic · Huyen (ch. agents) | request → tool_use → نفّذ → tool_result → رد |
| ذاكرة المحادثة (stateless API) | وثائق Anthropic (Multi-turn) | الـ API بلا حالة → تبعت التاريخ كامل كل مرة |
| تصميم الأدوات | shared/tool-use-concepts | أوصاف واضحة + متى تُستدعى |

> 🎯 **بيُستخدم في الواقع:** شات بوتس خدمة العملاء، المساعدين الشخصيين، الـ agents اللي بتنفّذ مهام.
> 🛠️ **هنا:** نبني الأدوات والذاكرة ونشغّلها **أوفلاين** بموجّه بسيط، والخلية الأخيرة تستخدم
> **Claude tool-use API الحقيقي** (محاطة بـ try/except عشان ما تكسرش النوتبوك بدون مفتاح).
""")

md("## 0️⃣ المكتبات وبيانات المتجر")
code("""import json, re, os

with open('data/shop_data.json', encoding='utf-8') as f:
    SHOP = json.load(f)

PRODUCTS = {p['name']: p for p in SHOP['products']}
ORDERS = SHOP['orders']
STORE = SHOP['store']
print('المنتجات:', list(PRODUCTS))
print('الطلبات:', list(ORDERS))""",
stub="""import json, re, os
with open('data/shop_data.json', encoding='utf-8') as f:
    SHOP = json.load(f)
# TODO: جهّز PRODUCTS (dict بالاسم) و ORDERS و STORE
PRODUCTS = ...
ORDERS = SHOP['orders']
STORE = SHOP['store']
print(list(PRODUCTS))""")

md(r"""## 1️⃣ الأدوات (Tools) — دوال بايثون حقيقية
كل أداة دالة بترجّع نص. دي الكود اللي النموذج "بيستدعيه" لمّا يحتاج معلومة حقيقية.""")
code('''def get_order_status(order_id):
    o = ORDERS.get(order_id.upper())
    if not o:
        return f"مفيش طلب بالرقم {order_id}."
    eta = "تم التسليم" if o['status'] == 'delivered' else (
          "ملغي" if o['status'] == 'cancelled' else f"متوقّع خلال {o['eta_days']} يوم")
    return f"الطلب {order_id.upper()}: الحالة={o['status']}، المنتجات={o['items']}، الإجمالي=${o['total']:.2f}، ({eta})."

def get_product_price(product_name):
    p = PRODUCTS.get(product_name)
    if not p:
        return f"المنتج '{product_name}' مش موجود."
    return f"{product_name}: ${p['price']:.2f}"

def check_stock(product_name):
    p = PRODUCTS.get(product_name)
    if not p:
        return f"المنتج '{product_name}' مش موجود."
    return f"{product_name}: متوفّر ({p['stock']} قطعة)" if p['stock'] > 0 else f"{product_name}: نفد من المخزون."

def calculate(expression):
    if not re.fullmatch(r"[\\d\\s+\\-*/().]+", expression):
        return "تعبير غير صالح."
    try:
        return f"{expression} = {eval(expression, {'__builtins__': {}}, {})}"
    except Exception:
        return "تعذّر حساب التعبير."

def store_info():
    return f"{STORE['name']} — المواعيد: {STORE['hours']}. للتواصل: {STORE['support_email']}."

DISPATCH = {'get_order_status': get_order_status, 'get_product_price': get_product_price,
            'check_stock': check_stock, 'calculate': calculate, 'store_info': store_info}
print(get_order_status('ORD1001'))
print(get_product_price('Laptop'))
print(check_stock('Headset'))''',
stub='''# TODO: عرّف الأدوات: get_order_status, get_product_price, check_stock, calculate, store_info
def get_order_status(order_id): ...
def get_product_price(product_name): ...
def check_stock(product_name): ...
def calculate(expression): ...
def store_info(): ...
DISPATCH = {...}
print(get_order_status('ORD1001'))''')

md(r"""## 2️⃣ مخطّطات الأدوات (Tool Schemas — صيغة Anthropic)
دي اللي بتتبعت للنموذج عشان يعرف الأدوات المتاحة ومدخلاتها. **الوصف لازم يقول "متى تُستخدم"**.""")
code('''TOOLS = [
    {"name": "get_order_status",
     "description": "ابحث عن حالة طلب عميل. استخدمها لما العميل يسأل عن طلب برقم مثل ORD1001.",
     "input_schema": {"type": "object",
        "properties": {"order_id": {"type": "string", "description": "رقم الطلب، مثل ORD1001"}},
        "required": ["order_id"]}},
    {"name": "get_product_price",
     "description": "ارجع سعر منتج. استخدمها لما العميل يسأل عن سعر/تكلفة منتج.",
     "input_schema": {"type": "object",
        "properties": {"product_name": {"type": "string"}}, "required": ["product_name"]}},
    {"name": "check_stock",
     "description": "تحقّق من توفّر منتج في المخزون. استخدمها لما العميل يسأل هل المنتج متاح.",
     "input_schema": {"type": "object",
        "properties": {"product_name": {"type": "string"}}, "required": ["product_name"]}},
    {"name": "calculate",
     "description": "احسب تعبيراً حسابياً (مثل مجموع أسعار). استخدمها لأي عملية حسابية.",
     "input_schema": {"type": "object",
        "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
    {"name": "store_info",
     "description": "ارجع مواعيد المتجر وبيانات التواصل. استخدمها للأسئلة العامة عن المتجر.",
     "input_schema": {"type": "object", "properties": {}}},
]
print(f'{len(TOOLS)} أدوات معرّفة')''',
stub='''# TODO: عرّف TOOLS كقائمة بصيغة Anthropic (name, description, input_schema) لكل أداة
TOOLS = [ ... ]
print(len(TOOLS))''')

md(r"""## 3️⃣ شات بوت بذاكرة (offline) — يشتغل بدون مفتاح API
بدل النموذج، موجّه (router) بسيط بيقرّر الأداة من الكلمات المفتاحية. الأهم هنا: **الذاكرة** —
بنحفظ تاريخ المحادثة + سياق (آخر طلب اتكلّمنا عنه) عشان نرد على الأسئلة المتابِعة.""")
code('''def route(msg, context):
    m = msg.lower()
    order = re.search(r'ord\\d+', m)
    if order:
        return 'get_order_status', {'order_id': order.group().upper()}
    if any(k in m for k in ['هيوصل', 'يوصل', 'arrive', 'eta', 'حالة طلبي']) and context.get('last_order'):
        return 'get_order_status', {'order_id': context['last_order']}   # ← ذاكرة السياق
    for name in PRODUCTS:
        if name.lower() in m:
            if any(k in m for k in ['سعر', 'بكام', 'price', 'cost', 'تكلفة']):
                return 'get_product_price', {'product_name': name}
            if any(k in m for k in ['متاح', 'متوفر', 'مخزون', 'stock', 'available']):
                return 'check_stock', {'product_name': name}
    if any(k in m for k in ['مواعيد', 'مفتوح', 'hours', 'email', 'تواصل']):
        return 'store_info', {}
    if re.search(r'\\d[\\d\\s+\\-*/().]*[+\\-*/]', m):
        return 'calculate', {'expression': re.search(r'[\\d\\s+\\-*/().]{3,}', m).group().strip()}
    return None, None

class ToolChatBot:
    def __init__(self):
        self.history = []      # ذاكرة المحادثة الكاملة
        self.context = {}      # حالة (آخر طلب، إلخ)

    def send(self, user_msg):
        self.history.append({'role': 'user', 'content': user_msg})
        name, args = route(user_msg, self.context)
        if name:
            reply = DISPATCH[name](**args)
            if name == 'get_order_status':
                self.context['last_order'] = args['order_id']   # حدّث السياق
        else:
            reply = "ممكن أساعدك في: حالة طلب (ORD####)، سعر/توفّر منتج، عملية حسابية، أو مواعيد المتجر."
        self.history.append({'role': 'assistant', 'content': reply})
        return reply

bot = ToolChatBot()
for turn in ["سعر الـ Laptop كام؟",
             "وحالة الطلب ORD1001؟",
             "هيوصل إمتى؟",                       # ← بيعتمد على الذاكرة (آخر طلب)
             "الـ Headset متاح؟",
             "احسبلي 1200 + 45"]:
    print(f"👤 {turn}")
    print(f"🤖 {bot.send(turn)}\\n")
print(f"📝 طول الذاكرة: {len(bot.history)} رسالة")''',
stub='''# TODO: اكتب router(msg, context) + كلاس ToolChatBot فيه history و context
#       استخدم context['last_order'] للأسئلة المتابِعة (الذاكرة)
def route(msg, context): ...
class ToolChatBot: ...
bot = ToolChatBot()
print(bot.send("سعر الـ Laptop كام؟"))''')

md(r"""## 4️⃣ (إنتاج) الشات بوت بـ Claude API الحقيقي — حلقة استدعاء الأدوات
دي الحلقة الفعلية: نبعت الرسالة + الأدوات → لو النموذج طلب أداة (`stop_reason == "tool_use"`) ننفّذها
ونرجّع `tool_result` → نكرّر لحد ما يخلّص. محاطة بـ try/except عشان تتخطّى أوفلاين بدون مفتاح.""")
code('''def chat_with_claude(user_msg, history=None, model="claude-opus-4-8"):
    """شات بوت إنتاجي باستدعاء أدوات حقيقي. يتطلب ANTHROPIC_API_KEY.
       (للتجارب الأرخص بدّل model إلى "claude-haiku-4-5".)"""
    try:
        import anthropic                                   # pip install anthropic
        client = anthropic.Anthropic()                     # يقرأ ANTHROPIC_API_KEY من البيئة
        messages = list(history or [])
        messages.append({"role": "user", "content": user_msg})

        while True:
            resp = client.messages.create(
                model=model, max_tokens=1024,
                system="أنت مساعد متجر TechNest. استخدم الأدوات لجلب بيانات حقيقية، وردّ بالعربية باختصار.",
                tools=TOOLS, messages=messages)

            if resp.stop_reason != "tool_use":
                return next((b.text for b in resp.content if b.type == "text"), ""), messages

            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    out = DISPATCH[block.name](**block.input)        # نفّذ نفس أدواتنا
                    tool_results.append({"type": "tool_result",
                                         "tool_use_id": block.id, "content": str(out)})
            messages.append({"role": "user", "content": tool_results})
    except Exception as e:
        return (f"[تم تخطّي Claude API: {type(e).__name__}] — شغّل النسخة الأوفلاين بالأعلى. "
                f"للإنتاج: pip install anthropic + ضبط ANTHROPIC_API_KEY."), (history or [])

answer, _ = chat_with_claude("الطلب ORD1002 حالته إيه، وإجمالي سعر Laptop + Monitor كام؟")
print(answer)''')

md(r"""## 5️⃣ الخلاصة والتوصيات (Conclusion)
- **استدعاء الأدوات (Tool Use)** بيربط النموذج ببيانات/أفعال حقيقية — مفيش "اختراع" معلومات.
- **الذاكرة:** الـ API بلا حالة (stateless)، فبنبعت تاريخ المحادثة كامل كل مرة؛ والسياق (آخر طلب)
  بيخلّي الردود المتابِعة منطقية.
- **الحلقة الوكيلة:** `request → tool_use → نفّذ → tool_result → رد` هي قلب أي **agent**.
- **النسخة الأوفلاين** أثبتت المعمار كامل بدون مفتاح؛ **نسخة الإنتاج** بتستخدم Claude الحقيقي بنفس الأدوات.
- **للإنتاج:** أضف معالجة أخطاء الأدوات (`is_error`)، حدود لعدد اللفّات، وتسجيل (logging)،
  ولو الأدوات كتير استخدم **Tool Search**.

> ✅ **اللي اتعلمته:** تعريف الأدوات، حلقة الـ tool-use، ذاكرة المحادثة، وربط نموذج حقيقي بأدوات بايثون.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "d3_chatbot_tools")
