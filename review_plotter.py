import pandas as pd
import os
import matplotlib.pyplot as plt

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
                values=filtered_df["profile"].value_counts()
                values.plot(kind="bar")
                plt.show()

            else: 

                print("Wrong data has been given")


        