# Vercel + OpenAI Minimal API (Bengali)

এই প্রজেক্টে একটি মিনিমাল Vercel Serverless API আছে যেটা OpenAI (ChatGPT) API-কে প্রোক্সি করে। আপনি আপনার `OPENAI_API_KEY` দিয়ে এটাকে ডেপ্লয় করে যেকোন ফ্রন্টএন্ড বা থার্ড-পার্টি অ্যাপ থেকে কল করতে পারবেন।

## কী আছে
- `api/chat.js`: POST এন্ডপয়েন্ট, `messages` বা `input` নিয়ে OpenAI-তে কল করে রিপ্লাই দেয়
- `vercel.json`: Node.js 18 রানটাইম সেটিংস
- `package.json`: `openai` SDK ডিপেন্ডেন্সি (ESM)

## ডেপ্লয় স্টেপস (Vercel)
1) এই ফোল্ডারটি GitHub/GitLab/Bitbucket এ পুশ করুন (বা Vercel CLI দিয়ে ডেপ্লয় করুন)।
2) Vercel Project-এ Environment Variable যোগ করুন:
   - Key: `OPENAI_API_KEY`
   - Value: আপনার OpenAI API key
   - Target: Production (আর চাইলে Preview/Development)
3) Deploy করুন। ডেপ্লয় হলে আপনার এন্ডপয়েন্ট হবে: `https://<your-app>.vercel.app/api/chat`

ঐচ্ছিক: যদি নির্দিষ্ট Origin ছাড়া অন্য কোথাও থেকে কল ব্লক করতে চান, `CORS_ORIGIN` ভ্যারিয়েবল যোগ করুন এবং সেট করুন আপনার ফ্রন্টএন্ড ডোমেইন (যেমন `https://example.com`)।

## এন্ডপয়েন্ট ব্যবহার
- Method: `POST`
- URL: `/api/chat`
- Body (JSON):
  - `messages`: OpenAI Chat messages array (role/content)
  - অথবা `input`: সিম্পল ইউজার স্ট্রিং
  - `system`: ঐচ্ছিক সিস্টেম প্রম্পট
  - `model`: ঐচ্ছিক (ডিফল্ট `gpt-4o-mini`)
  - `temperature`, `max_tokens`: ঐচ্ছিক

### উদাহরণ (cURL)
```
curl -X POST "https://<your-app>.vercel.app/api/chat" \
  -H "content-type: application/json" \
  -d '{
    "input": "বাংলায় ৩টি প্রেরণাদায়ী উক্তি দাও"
  }'
```

### উদাহরণ (messages সহ)
```
curl -X POST "https://<your-app>.vercel.app/api/chat" \
  -H "content-type: application/json" \
  -d '{
    "messages": [
      {"role":"system","content":"You are a helpful assistant."},
      {"role":"user","content":"হ্যালো, তুমি কেমন আছো?"}
    ]
  }'
```

### ফ্রন্টএন্ড থেকে কল (fetch)
```
const res = await fetch("https://<your-app>.vercel.app/api/chat", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ input: "বাংলায় একটা ছোট গল্প বলো" })
});
const data = await res.json();
console.log(data.message?.content);
```

## নোট
- আপনার OpenAI key কখনোই ফ্রন্টএন্ড/ব্রাউজারে এক্সপোজ করবেন না। এই API-টাই প্রোক্সি হিসেবে ব্যবহার করুন।
- স্ট্রীমিং প্রয়োজন হলে এই এন্ডপয়েন্টে পরে server-sent events/edge runtime যুক্ত করা যাবে।
- প্রয়োজন হলে `model` হিসেবে `gpt-4o`, `gpt-4o-mini`, `o4-mini` ইত্যাদি ব্যবহার করতে পারেন (আপনার অ্যাক্সেস অনুযায়ী)।

```
ফাইলসমূহ:
- api/chat.js
- package.json
- vercel.json
```
