import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(layout="wide")

class ReviewPlotter:

    def __init__(self,directory="processed_data",filename="review_data.csv"): 

        if os.path.exists(os.path.join(directory, filename)):
            self.data=pd.read_csv(f"{directory}/{filename}")
        
        else:
            print("Error while loading the file")


    def show_repartition(self,palier_criteria=None,order_label_criteria=None,neg_threshold=3,pos_threshold=4):

            def reviewer_profile(x):
                if pd.isnull(x):
                    return "Unknown"
                elif x>=pos_threshold:
                    return "Promoter"
                elif x<neg_threshold:
                    return "Detractor"
                else:
                    return "Neutral"

            self.data["profile"]=self.data["average_review_score"].apply(lambda x: reviewer_profile(x))
            filtered_df=self.data.copy()

            if(palier_criteria):
                filtered_df=filtered_df[filtered_df["palier"]==palier_criteria]

            if(order_label_criteria):
                filtered_df=filtered_df[filtered_df["order_label"]==order_label_criteria]        
        
            if("profile" in filtered_df.columns):
                values = filtered_df["profile"].value_counts().reset_index()
                values.columns = ['profile', 'count']

                # Plotting the pie chart using Plotly Express
                fig = px.pie(values, values='count', names='profile', title="Profile Distribution")
                st.plotly_chart(fig)

            else: 

                print("Wrong data has been given")


review_plotter = ReviewPlotter()

# df_order_payments = pd.read_csv("Data\olist_order_payments_dataset.csv")
df_final = pd.read_csv("C:/Users/anton/Desktop/Data/Master2/data_app_automatisation/data_final.csv")
df_grouped = pd.read_csv("C:/Users/anton/Desktop/Data/Master2/data_app_automatisation/df_group.csv")


df_grouped['customer_city'] = df_final['customer_city']
df_grouped['customer_state'] = df_final['customer_state']

df_final['date_only'] = pd.to_datetime(df_final['order_date']).dt.date
# FONCTION KPI 

# Fonction pour créer le graphique en fonction du filtre
def plot_top_objects_label(filter_value):
    # Filtrer les données en fonction de la valeur de filtrage
    filtered_data = df_final[df_final['order_label'] == filter_value]

    # Compter les occurrences de chaque objet
    top_objects = filtered_data['product_category_name'].value_counts().head(10)

    # Créer le graphique à barres avec plotly express
    fig = px.bar(top_objects, x=top_objects.index, y=top_objects.values, color=top_objects.values,
                 labels={'x': 'Objets', 'y': "Nombre d'occurrences"})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

# Fonction pour créer le graphique en fonction du filtre
def plot_top_objects_palier(filter_value):
    # Filtrer les données en fonction de la valeur de filtrage
    filtered_data = df_final[df_final['palier'] == filter_value]

    # Compter les occurrences de chaque objet
    top_objects = filtered_data['product_category_name'].value_counts().head(10)

    # Créer le graphique à barres avec plotly express
    fig = px.bar(top_objects, x=top_objects.index, y=top_objects.values, color=top_objects.values,
                 labels={'x': 'Objets', 'y': "Nombre d'occurrences"})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

def plot_top_objects_synthese(filter_city=None, filter_region=None):
    # Filtrer les données si des filtres sont spécifiés
    if filter_city and filter_region:
        filtered_data = df_final_synthese[(df_final_synthese['customer_city'] == filter_city) & (df_final_synthese['customer_state'] == filter_region)]
    else:
        filtered_data = df_final_synthese

    # Compter les occurrences de chaque objet
    top_objects = filtered_data['product_category_name'].value_counts().head(10)

    # Créer le graphique à barres avec Plotly Express
    fig = px.bar(top_objects, x=top_objects.index, y=top_objects.values, color=top_objects.values,
                 labels={'x': 'Objets', 'y': "Nombre d'occurrences"})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

def plot_saisonalite(filter_city=None, filter_region=None):
    # Filtrer les données si des filtres sont spécifiés
    if filter_city and filter_region:
        filtered_data = df_final_synthese[(df_final_synthese['customer_city'] == filter_city) & (df_final_synthese['customer_state'] == filter_region)]
    else:
        filtered_data = df_final_synthese

    # Convertir la colonne 'order_date' en datetime
    filtered_data['order_date'] = pd.to_datetime(filtered_data['order_date'])

    # Extraire le mois et l'année à partir de la colonne 'order_date'
    filtered_data['month'] = filtered_data['order_date'].dt.month
    filtered_data['year'] = filtered_data['order_date'].dt.year

    # Séparer les données par année
    df_2017 = filtered_data[filtered_data['year'] == 2017]
    df_2018 = filtered_data[filtered_data['year'] == 2018]

    # Calculer les totaux pour chaque année
    total_prices_2017 = df_2017.groupby('month')['price_y'].sum().reset_index(name='total_prices')
    total_prices_2018 = df_2018.groupby('month')['price_y'].sum().reset_index(name='total_prices')

    # Créer le graphique avec Plotly Express
    fig = px.line()
    fig.add_scatter(x=total_prices_2017['month'], y=total_prices_2017['total_prices'], mode='lines+markers', name='2017')
    fig.add_scatter(x=total_prices_2018['month'], y=total_prices_2018['total_prices'], mode='lines+markers', name='2018')

    # Mise en forme du graphique
    fig.update_layout(title='Total des ventes par mois',
                      xaxis_title='Mois',
                      yaxis_title='Total des ventes (en real)',
                      legend_title='Année',
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      showlegend=True,
                      hovermode='x unified')
    
    # Afficher le graphique
    st.plotly_chart(fig)

def plot_heure(filter_city=None, filter_region=None):
    if filter_city and filter_region:
        filtered_data = df_final_synthese[(df_final_synthese['customer_city'] == filter_city) & (df_final_synthese['customer_state'] == filter_region)]
    else:
        filtered_data = df_final_synthese

    filtered_data["heure"] = filtered_data["order_date"].dt.hour

    grouped = filtered_data.groupby(['heure', 'product_category_name']).size().reset_index(name='count')

    # Trouver l'index de la ligne avec le nombre maximal d'occurrences pour chaque heure
    max_count_indices = grouped.groupby('heure')['count'].idxmax()

    # Obtenir les lignes correspondant aux indices trouvés
    most_common_categories = grouped.loc[max_count_indices]
    fig = px.bar(most_common_categories, x='heure', y='count', color='product_category_name', title="Catégories de produits les plus courantes par heure")
    st.plotly_chart(fig)
    # st.write(most_common_categories)

    # total = filtered_data.groupby('heure')['product_category_name'].nunique().reset_index(name='total_type_produit')
    # fig = px.bar(filtered_data, x=filtered_data['heure'], y=total)
    # fig.update_xaxes(tickangle=45)
    # st.plotly_chart(fig)
    

def mode_paiement_commande(filtre):
    order_payment_1 = df_grouped[df_grouped['order_label'] == filtre]['payment_type'].value_counts(normalize=True) * 100
    fig = px.pie(names=order_payment_1.index, values=order_payment_1.values)
    st.plotly_chart(fig)

def mode_paiement_prix(filtre):
    #Catégorie 1
    price_payment_1 = df_grouped[df_grouped['palier'] == filtre]['payment_type'].value_counts(normalize=True) * 100
    fig4 = px.pie(names=price_payment_1.index, values=price_payment_1.values)
    st.plotly_chart(fig4)

df_final["order_label"] = df_final["order_label"].astype(str)

def top_villes_par_nombre_clients(df):
    top_villes = df.groupby('customer_city')['customer_id'].nunique().sort_values(ascending=False).head(10)
    return top_villes


def top_villes_par_nombre_clients_filtre(filtre):

    df_filtered = df_final[df_final["order_label"] == filtre]
    top_10_villes_clients = top_villes_par_nombre_clients(df_filtered)
    return top_10_villes_clients



df_final["Total_amount"] = df_final.apply(lambda x: x["price_y"] + x["freight_value"], axis=1)

def top_villes_CA(df):
    top_villes_CA = df.groupby('customer_city')['Total_amount'].sum().sort_values(ascending=False).head(10)
    return top_villes_CA

def top_villes_CA_filtre(filtre):
    df_filtered_2 = df_final[df_final["palier"] == filtre]
    top_10_villes_CA = top_villes_CA(df_filtered_2)
    return top_10_villes_CA

def nb_cmd_page(filtre):
        st.subheader("Pourcentage de promoteur/neutre/détracteur")
        review_plotter.show_repartition(order_label_criteria=filtre)

        st.subheader("TOP 10 catégories de produits")
        plot_top_objects_label(filtre)

        st.subheader("Prix moyen des paniers")
        avg_basket_order_1 = df_grouped[df_grouped['order_label'] == filtre]['price_y'].mean()
        med_basket_order_1 = df_grouped[df_grouped['order_label'] == filtre]['price_y'].median()
        st.metric(label="valeur moyenne :", value=avg_basket_order_1)
        st.metric(label="valeur median :", value=med_basket_order_1)


        st.subheader("TOP 10 villes par nombre de clients")
        st.write(top_villes_par_nombre_clients_filtre(filtre=filtre))

        st.subheader("Mode de paiement les plus utilisés")
        mode_paiement_commande(filtre=filtre)

def prix_page(filtre):
        st.subheader("Pourcentage de promoteur/neutre/détracteur")
        review_plotter.show_repartition(palier_criteria=filtre)

        st.subheader("TOP 10 catégories de produits")
        plot_top_objects_palier(filtre)


        kpi_1, kpi_2 = st.columns(2)
        with kpi_1:
                st.subheader("Prix moyen des paniers")
                avg_basket_price_1 = df_grouped[df_grouped['palier'] == filtre]['price_y'].mean()
                med_basket_price_1 = df_grouped[df_grouped['palier'] == filtre]['price_y'].median()
                st.metric(label="valeur moyenne :", value=avg_basket_price_1)
                st.metric(label="valeur median :", value=med_basket_price_1)

        with kpi_2:
                st.subheader("Nombre d'articles moyen des paniers")
                avg_nb_article_moyen_price_1 = round(df_grouped[df_grouped['palier'] == filtre]['nb_article_panier'].mean(),2)
                st.metric(label='Valeur moyenne :', value = avg_nb_article_moyen_price_1)

        st.subheader("TOP 10 villes par CA")
        st.write(top_villes_CA_filtre(filtre=filtre))

        st.subheader("Mode de paiement les plus utilisés")
        mode_paiement_prix(filtre)



# SIDEBAR 
with st.sidebar:
    
    # st.image('pngegg.png')
    st.title('🌸 Olist Customer Analysis')
    st.write("**Les filtres s'aplliquent seulement pour l'onglet synthèse**")
    # FILTRE State 
    unique_state = ['Tous'] + sorted(df_final['customer_state'].unique())
    selected_state = st.selectbox('**Sélectionnez une région**', unique_state)
    # FILTRE CITY 
    unique_cities = ['Tous'] + sorted(df_final['customer_city'].unique())
    selected_city = st.selectbox('**Sélectionnez une ville**', unique_cities)

        # Filtrage du DataFrame en fonction des sélections de l'utilisateur
    if selected_state == 'Tous' and selected_city == 'Tous':
        df_final_synthese = df_final  # Aucun filtre appliqué
    elif selected_state == 'Tous':
        df_final_synthese = df_final[df_final['customer_city'] == selected_city]
    elif selected_city == 'Tous':
        df_final_synthese = df_final[df_final['customer_state'] == selected_state]
    else:
        df_final_synthese = df_final.query("(customer_state == @selected_state) and (customer_city == @selected_city)")
        
    if selected_state == 'Tous' and selected_city == 'Tous':
        df_final_synthese_2 = df_grouped  # Aucun filtre appliqué
    elif selected_state == 'Tous':
        df_final_synthese_2 = df_grouped[df_grouped['customer_city'] == selected_city]
    elif selected_city == 'Tous':
        df_final_synthese_2 = df_grouped[df_grouped['customer_state'] == selected_state]
    else:
        df_final_synthese_2 = df_grouped.query("(customer_state == @selected_state) and (customer_city == @selected_city)")
    
    

#  PAGE PRINCIPAL 
nb_cmd, prix, synthese = st.tabs(['Nombre de commandes','Prix dépensé','Synthèse']) 

with nb_cmd:
    with st.expander("Segmentation des clients en 3 catégories :"):
        st.write("client avec : **1 commande**")
        st.write("client avec : **2 commandes**")
        st.write("client avec : **3 commandes ou plus**")
    
    cmd_1, cmd_2, cmd_3_plus = st.tabs(['1 commande','2 commandes','3 commandes ou plus']) 

    with cmd_1:
       nb_cmd_page(filtre='1')

    with cmd_2:
        nb_cmd_page(filtre='2')

    with cmd_3_plus:
        nb_cmd_page(filtre='3+')

with prix:
    with st.expander("Segmentation des clients en 4 catégories :"):
        st.write("clients ayant dépensé : **0 à 49.99€**")
        st.write("clients ayant dépensé : **50 à 99.99€**")
        st.write("clients ayant dépensé : **100 à 149.99€**")
        st.write("clients ayant dépensé : **150€ ou plus**")

    cat_1, cat_2, cat_3, cat_4 = st.tabs(['0 à 49.99€','50 à 99.99€','100 à 149.99€','150€ ou plus']) 

    with cat_1:
        prix_page(filtre='Moins de 50')

    with cat_2:
        prix_page(filtre='50-99.99')

    with cat_3:
        prix_page(filtre='100-149.99')

    with cat_4:
        prix_page(filtre='Plus de 150')

with synthese:
    st.subheader('Panier moyen')
    average_price = df_final_synthese_2['price_y'].mean()
    median_price = df_final_synthese_2['price_y'].median()
    st.metric(label="valeur moyenne :", value=average_price)
    st.metric(label="valeur median :", value=median_price)

    st.subheader(f'Nombre de commandes dans la ville : {selected_city}')
    if selected_city =='Tous':
        st.write('**Veuillez selectionner une ville**')
    else:
        filtre_city = df_final_synthese[['order_id', 'customer_state', 'customer_city']]
        filtre_city_2 = filtre_city.drop_duplicates()
        grouped = filtre_city.groupby(['customer_state', 'customer_city'])['order_id'].nunique().reset_index()
        df_result = grouped
        df_result = df_result.rename(columns={"order_id":"Total_commandes"})

        def nombre_commande_moyen(filter_city=None):

            if filter_city:
                df_filtered_3 = df_result[(df_result['customer_city'] == filter_city)]
            else:
                df_filtered_3 = df_result

            Nombre_commande_moyen = round(df_filtered_3['Total_commandes'].mean(),2)
            st.metric(label='valeur',value=Nombre_commande_moyen)

        nombre_commande_moyen()

    st.subheader("Nombre d'articles moyen des paniers")
    avg_nb_article_moyen_price = round(df_final_synthese_2['nb_article_panier'].mean(),2)
    st.metric(label='Valeur moyenne :', value = avg_nb_article_moyen_price)

    # st.subheader('Pourcentage de promoteur/neutre/détracteur')

    st.subheader('Moyen de paiement')
    price_payment = df_final_synthese_2['payment_type'].value_counts(normalize=True) * 100
    fig8 = px.pie(names=price_payment.index, values=price_payment.values)
    st.plotly_chart(fig8)

    st.subheader('Saisonnalité')
    plot_saisonalite()

    st.subheader('Catégories de produit par heure')
    plot_heure()
    # st.write(df_final.columns)


    st.subheader('TOP 10 catégories de produits')
    plot_top_objects_synthese()
