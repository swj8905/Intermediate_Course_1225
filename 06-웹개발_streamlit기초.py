import streamlit as st

st.text("Hello World")
st.text("Hello Python")

st.write("이런 것도 됩니다.")
st.write("# 이런 것도 됩니다.")
st.write("## 이런 것도 됩니다.")
st.write("### 이런 것도 됩니다.")
st.write("#### 이런 것도 됩니다.")
st.write("##### 이런 것도 됩니다.")
st.write("###### 이런 것도 됩니다.")

st.write("**이런** 것도 됩니다.")
st.write("*이런* 것도 됩니다.")

st.write("---------")

st.write([0,1,2,3])
st.write({"짜장면":1000, "짬뽕":2000})
st.write("1 + 1 = ", 2)

st.write("https://www.naver.com")

st.code("""
foo = 10
if foo >= 0:
    print("OK")
else foo < 0:
    print("NO")
""")

"이런 것도 됩니다."
"# 이런 것도 됩니다."
"## 이런 것도 됩니다."

"""
# 매직 커맨드

https://www.naver.com

|      |  점수   |   평가    |
|------|---------:|:-----------:|
| 철수 |90       |참잘했습니다.|
| 영희 |30       |분발해주세요.|

```python
print("Hello World")
```
------------

"""

st.image("https://w.namu.la/s/bf534326c82256e07ebcf3a115ed38f5e86a8fb61ea5db06aac1c5195b72e17db21c18b364865e765c22de9795a736590d630966d7d887a17a023fc6ce4bc7b3e6fa33322a215727df10002f4d1ae06b41cc18027fae6b6bce8187e715eed522")