import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import folium

from datetime import datetime
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

plt.style.use('science')
st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
	data = pd.read_csv(path)
	return data


def data_clean(data):
	# converção de date para o formato de data
	data['date'] = pd.to_datetime(data['date'])

	# checando se há dados duplicados 
	duplicate = data.duplicated().unique()
	a = print ('Dados duplicados:{}'.format(duplicate))

	# checando dados NA (se tiver algum valor NA ocorre True)
	null = data.isnull().values.any()
	b = print ('Dados nulos:{}'.format(null))

	return a, b


def data_overview(data):
	
	st.sidebar.image('fig1.jpg',  use_column_width=True)
	st.markdown("<h1 style='text-align: center; color: black;'> House Rocket Project </h1>", unsafe_allow_html=True)

	st.sidebar.write('Project objective: Find the best options to buy houses and show this to House Rocket CEO')

	if st.sidebar.checkbox('Show dataset sample'):
		#st.write(data.head(20))
		st.subheader('Initial dataset')
		st.dataframe(data.head(20))
	
	return None


def new_colunas(data):
	# criando coluna mês do ano 
	data['month'] = data['date'].dt.month

	# criando coluna renovated
	data['renovated'] = data['yr_renovated'].apply(lambda x: 'yes' if x>0 else 'no')

	# criando coluna das estações do ano segundo o hemisferio norte
	data['sesson'] = data['month'].apply(lambda x: 'spring' if 3<=x<=5 else
                                               'summer' if 6<=x<=8 else
                                               'fall' if 9<=x<=11 else 
                                               'winter')
	return data


def estatistica(data):
	# fazendo uma copia do dataset
	data_copy = data.copy()

	# dropando a coluna com quartos 33
	data_copy = data_copy.drop(15870)
	
	# trabalhando com variaveis numericas 
	data_num = data_copy.select_dtypes(include = ['int64', 'float64'])

	#deletando a coluna ID 
	data_num = data_num.iloc[:, 1: ]
	
	

	# estatistica descritiva
	data_num_mean = pd.DataFrame(data_num.apply(np.mean)).T
	data_num_median = pd.DataFrame(data_num.apply(np.median)).T
	data_num_std = pd.DataFrame(data_num.apply(np.std)).T
	data_num_max = pd.DataFrame(data_num.apply(np.max)).T
	data_num_min = pd.DataFrame(data_num.apply(np.min)).T

	# concatenando em um mesmo data frame
	data_descr = pd.concat([data_num_mean, data_num_median, data_num_std, data_num_max, data_num_min]).T.reset_index()

	# renomeando as colunas
	data_descr.columns = ['attributes', 'mean', 'median', 'std', 'max', 'min']

	if st.sidebar.checkbox('Descriptive analysis'):
		st.subheader('Descriptive analysis')
		st.dataframe(data_descr)

	return None


def hypo_test(data):
	# fazendo uma copia do dataset
	data2_copy = data.copy()

	st.markdown("<h1 style='text-align: center; color: black;'> Hyphotesis tests </h1>", unsafe_allow_html=True)

	# hipoteses
	st.write('H1: Houses prices grow 10 % MoM on average')
	st.write('H2: Houses never renovated are 15% cheaper on average')
	st.write('H3: The summer season has prices 30% more expensive on average than the other seasons of the year')
	st.write('H4: Houses with a water view in the summer season are 40% more expensive on average than those with a water view in the winter')
	st.write('H5: Houses with water views are on average 30% more expensive')

	c1,c2,c3 = st.beta_columns((1,1,1))

	# H1 = O preço dos imóveis crescem 10% MoM na média 
	c1.subheader('H1')
	h1 = data2_copy[['price', 'month']].groupby('month').mean().reset_index()

	#gráfico 
	fig1, ax = plt.subplots(figsize=(3, 3))
	plt.ylabel('Price')
	plt.xlabel('Months')
	plt.xticks( [i+1 for i, _ in enumerate(h1['month'])], h1['month'])
	plt.plot(h1['month'], h1['price'])
	c1.pyplot(fig1)

	# H2 = Imóveis nunca reformados são 15% mais baratos na média 
	c2.subheader('H2')
	
	h2 = data2_copy[['price', 'renovated']].groupby('renovated').mean().reset_index()

	# gráfico 
	fig2, ax = plt.subplots(figsize=(3, 3))
	plt.ylabel('Price')
	plt.xlabel('Renovated')
	plt.bar(h2['renovated'], h2['price'])
	c2.pyplot(fig2)

	# H3 = A estação summer apresenta preços 30% mais caros na média que as outras estações do ano
	c3.subheader('H3')
	h3 = data2_copy[['price', 'sesson']].groupby('sesson').mean().reset_index()

	#gráfico 
	fig3, ax = plt.subplots(figsize=(3, 3))
	plt.ylabel('Price')
	plt.xlabel('Seasson')
	plt.bar(h3['sesson'], h3['price'])
	c3.pyplot(fig3)
	
	c4,c5 = st.beta_columns((1,1))

	# H4 = Os imóveis com vista para água na estação summer são 40% na média mais caros que os com vista para aguá no winter 
	c4.subheader('H4')
	df = data2_copy.loc[data2_copy['waterfront']==1, ['price', 'sesson']].reset_index()
	h4 = df[['price', 'sesson']].groupby('sesson').mean().reset_index()

	# selecionando só winter e summer do dataframe h4
	h4_ = h4.loc[ (h4['sesson']=='summer') | (h4['sesson']=='winter'), 'price'].reset_index()

	#gráfico 
	fig4, ax = plt.subplots(figsize=(4, 2))
	plt.ylabel('Price')
	plt.xlabel('Seasson')
	plt.bar(['Summer', 'Winter'], h4_['price'])
	c4.pyplot(fig4)

	# H5 = Imóveis com vista para água são em média 30% mais caros
	c5.subheader('H5')
	h5 = data2_copy[['price', 'waterfront']].groupby('waterfront').mean().reset_index()

	# gráfico 
	fig5, ax = plt.subplots(figsize=(4, 2))
	plt.ylabel('Price')
	plt.xlabel('Waterview')
	plt.bar(['No', 'yes'], h5['price'])
	c5.pyplot(fig5)

	return None


def questoes(data):
	# fazendo uma copia do dataset
	data_copy = data.copy()

	st.markdown("<h1 style='text-align: center; color: black;'> Business issues  </h1>", unsafe_allow_html=True)
	
	st.subheader ('What properties should the CEO buy and what is the purchase price? ')

	# Quais são os imóveis que deveria comprar e por qual preço?
	data_median = data_copy[['zipcode', 'price']].groupby('zipcode').median().reset_index()

	df = data_copy.copy()

	df_merge = pd.merge(data_median, df, on='zipcode', how = 'inner')

	# renomeando price_x e price_y
	df_merge = df_merge.rename(columns = {'price_y' : 'price', 'price_x' : 'price_median'} )

	# classificando os imoveis a serem comprados tenha preço menor que a mediana de cada regiao e estejam em boas condições
	for i, row in df_merge.iterrows():
		if (row['price_median'] >= row['price']) & (row['condition'] > 3):
			df_merge.loc[i, 'buy'] = 'yes'
		else:
			df_merge.loc[i, 'buy'] = 'no'
			
	# salvando apenas as colunas que me interessa
	data_resume = df_merge[['id', 'zipcode', 'price', 'price_median', 'condition','sesson', 'lat', 'long', 'buy']]

	# criando checkbox para mostrar dataset
	if st.sidebar.checkbox('Houses classification'):
		st.subheader('Houses classifation by buy or not buy')
		st.dataframe(data_resume)
	
	data_resume_mapa = data_resume.copy()
	data_resume_mapa = data_resume_mapa[data_resume_mapa['buy']=='yes']
	
	st.write('House map just to buy ')
	
	

	#construção do mapa
	mapa = folium.Map(location =[data_resume_mapa['lat'].mean(), data_resume_mapa['long'].mean()], default_zoom_start=30)

	marker_cluster= MarkerCluster().add_to(mapa)

	for name, row in data_resume_mapa.iterrows():
		folium.Marker([row['lat'], row['long']], popup='Price: {}'.format(row['price'])).add_to(marker_cluster)

	
	col1, col2, col3 = st.beta_columns([1,2,1])

	with col1:
		st.write("")

	with col2:
		folium_static(mapa)

	with col3:
		st.write("")
	#-----------------------------------------------------------------------------------------
	
	st.subheader ('After properties have been purchased, when is the best time to sell them and at what prices?')

	# Uma vez comprado, qual é o melhor momento para vendê-lo e por qual preço?
	data_resume2 = data_resume.copy()

	# selecionando apenas as linhas com buy = yes
	data_resume2 = data_resume2[data_resume2['buy']=='yes']

	# mediana do preço para cada estação dentro de cada zipcode
	df_buy_sell = data_resume2[['sesson', 'zipcode', 'price']].groupby(['zipcode', 'sesson']).median().reset_index()

	# juntando os dataset com as colunas do nosso interesse 
	df_buy_sell_final = pd.merge(data_resume2, df_buy_sell, on='zipcode', how = 'inner')

	# renomeando as colunas do dataset final 
	df_buy_sell_final = df_buy_sell_final.rename(columns = {'price_x' : 'price', 'sesson_x': 'season', 'sesson_y': 'season_meadian', 'price_y':'price_median_season'} )

	# estipulando o preço de venda para cada imóvel 
	for i, row in df_buy_sell_final.iterrows():
		if (row['price_median_season'] > row['price']):
			df_buy_sell_final.loc[i, 'sale'] =  row['price'] * 1.1
		else:
			df_buy_sell_final.loc[i, 'sale'] = row['price'] * 1.3

	# calculo da coluna lucro
	df_buy_sell_final['lucro'] = df_buy_sell_final['sale'] - df_buy_sell_final['price']

	# criando checkbox para mostrar dataset
	if st.sidebar.checkbox('Final dataset'):
		st.subheader('Buy, sell and profit price ')
		st.dataframe(df_buy_sell_final)

	# plotando grafico final
	fig_final = px.bar(df_buy_sell_final, x = 'season', y = 'sale', color = 'season', labels={'season':'Season', 'sale': 'Sell price'})

	fig_final.update_layout(showlegend = False)

	st.plotly_chart(fig_final, x='season', y='sale', use_container_width= True)

	
	#-----------------------------------------------------------------------------------------
	
	# lucro total para a empresa
	#st.header('Estimate profit')
	#st.write(round(df_buy_sell_final['lucro'].sum(), 3))

	# conclusões
	st.markdown("<h1 style='text-align: center; color: black;'> Conclusions </h1>", unsafe_allow_html=True)

	st.write('Hypotheses H2 and H5 are true. If the proposed homes are bought and sold at the right time it will generate an estimated profit of 1,300,434,878.80 ')

	st.sidebar.write('To learn more and access the repository github')

	return None


if __name__ == "__main__":

	path = 'kc_house_data.csv'
	data = get_data(path)
	
	data_clean(data)
	data_overview(data)
	new_colunas(data)

	estatistica(data)
	hypo_test(data)
	questoes(data)
	
