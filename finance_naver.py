import pandas as pd
import warnings
import matplotlib.pyplot as plt
import streamlit as st
warnings.filterwarnings('ignore')



def get_exchange_rate_data(code, currency_name) :
    plt.rc('font', family='Malgun Gothic')
    df = pd.DataFrame()
    
    for page_num in range(1,6):
        base_url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"
        tamp = pd.read_html(base_url, encoding='cp949', header=1)
        
        df = pd.concat([df, tamp[0]])
        
    total_rate_data_view(df, code, currency_name)


def total_rate_data_view(df, code, currency_name) :
    # 원하는 열만 추출
    df_total = df[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]

    # 데이터 표시
    # print(f'=========={currency_name[code_in]}-{code}==========')
    # print(df_total.head(20))
    
    # 웹앱에 뿌리기 위한 처리
    st.subheader(f'{currency_name} : {code}')
    st.dataframe(df_total.head(20))

    # 전체 차트작성
    df_total_chart = df_total.copy()
    df_total_chart = df_total_chart.set_index('날짜')

    # 최신데이터와 과거데이터의 순서를 바꿈. 역순으로 표시
    df_total_chart=df_total_chart[::-1]
    ax = df_total_chart['매매기준율'].plot(figsize=(15, 6), title='Total exchange rate')
    fig = ax.get_figure()
    st.pyplot(fig)
    # plt.show()
    
#    month_rate_data_view(df_total)



# def month_rate_data_view(df_total) :
#     # 월별 검색
#     # 날짜 열 형변환(문자열 -> 날짜형식) 
#     df_total['날짜']=df_total['날짜'].str.replace(".","").astype('datetime64[ms]')

#     # '월' 파생변수 생성 
#     df_total['월'] = df_total['날짜'].dt.month
#     month_in = int(input('검색할 월 입력>>'))
#     month_df = df_total.loc[df_total['월'] == month_in, ['날짜', '매매기준율', '사실 때','파실 때',	'보내실 때','받으실 때'	]]

#     # 데이터 표시
#     print(f'=========={currency_name[code_in]}-{code}==========')
#     print(month_df.head(20))

#     # 인덱스 재조정
#     month_df = month_df.reset_index(drop=True)
#     month_df_chart = month_df.copy()
#     month_df_chart = month_df_chart.set_index('날짜')
#     month_df_chart['매매기준율'].plot(figsize=(15,6))
#     plt.show()


# code_in = int(input('통합유형 선택(1:USD, 2:EUR, 3:JPY)'))
# currency_symbols = ['USD', 'EUR', 'JPY']
# currency_name = ['미국 달러', '유럽연합 유로', '일본 엔(100)']
# code = currency_symbols[code_in-1]

# get_exchange_rate_data(code)


def exchange_main() :
    currency_symbols_name = {'미국 달러': 'USD', '유럽연합 유로': 'EUR', '일본 엔(100)': 'JPY'}
    currency_name = st.selectbox('통합선택', currency_symbols_name.keys())
    code =currency_symbols_name[currency_name]
    
    clicked = st.button('환률 데이터 가져오기')
    if clicked:
        get_exchange_rate_data(code, currency_name)
    
    
if __name__ == "__main__":
    exchange_main()