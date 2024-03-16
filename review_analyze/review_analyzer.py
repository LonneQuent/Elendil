import pandas as pd
import matplotlib.pyplot as plt

class ReviewAnalyzer: 

    

    def __init__(self):

        self.customer_data=pd.read_csv('raw_data/olist_customers_dataset.csv')
        self.review_data=pd.read_csv('raw_data/olist_order_reviews_dataset.csv')
        self.order_data=pd.read_csv('raw_data/olist_orders_dataset.csv')
        self.croisement=pd.read_csv('processed_data/table_croisement.csv')

    def compute_data(self):

        key_table=self.customer_data[["customer_id","customer_unique_id","customer_city","customer_state"]]
        merged_df=pd.merge(self.order_data,self.review_data,how="left",on="order_id")
        merged_df=pd.merge(merged_df,key_table,how="left",on="customer_id")

        average_note_per_customer=merged_df.groupby("customer_unique_id")["review_score"].mean().rename("average_review_score")
        number_note_per_customer=merged_df.groupby("customer_unique_id")["review_score"].count().rename("number_of_reviews")

        self.computed_df=pd.merge(merged_df,average_note_per_customer,how="left",right_index=True,left_on="customer_unique_id")
        self.computed_df=pd.merge(self.computed_df,number_note_per_customer,how="left",right_index=True,left_on="customer_unique_id")

        self.computed_df=pd.merge(self.computed_df,self.croisement,how="left",on="customer_id")
    
    def save_data(self,name):

        if hasattr(self,"computed_df"):
            self.computed_df.to_csv(f"processed_data/{name}")
        else: 
            print("You must compute the data first")

if __name__=='__main__':
    
    review_analyser=ReviewAnalyzer()
    review_analyser.compute_data()
    review_analyser.save_data("review_data.csv")
