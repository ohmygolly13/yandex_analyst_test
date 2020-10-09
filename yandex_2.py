import pandas as pd

def if_cross_segment(x,y,x0,y0,x1,y1):  
    #y0 > y1
    buf = y1
    y0.loc[y0 > y1] = y1
    y1.loc[buf < y0] = buf
     
    return ((y >= y0) & (y <= y1)) & (((x0 < x1) & (((y0 - y1) / (x1 - x0)) >= ((y1 - y) / (x1 - x)))) | ((x0 > x1) & (((y1 - y0) / (x0 - x1)) <= ((y1 - y) / (x - x1)))) | ((x0 == x1) & (x1 <= x)))
        
    
def if_belong_to_poly(x,y,points):
    cross_count = 0    
    for i in range(0,len(points) - 1):
        cross_count = cross_count + if_cross_segment(x,y,points[i][0],points[i][1],points[i+1][0],points[i+1][1]).astype(int)
    return cross_count % 2 > 0        

def main():
    df_poly = pd.read_csv('place_zone_coordinates.csv')
    df_users = pd.read_csv('user_coordinates.csv')
    df_poly = df_poly.pivot(index='place_id',columns = 'point_number')
    df_poly['key'] = 1
    df_users['key'] = 1
    df = df_poly.merge(df_users,on='key')
    df.drop(columns = ['key',('key','')],inplace=True)
    vertexes = (len(df.columns) - 3) / 2
    df['if_belong'] = if_belong_to_poly(df['loc_lat'],df['loc_lon'],[[df[('loc_lat',i)],df[('loc_lon',i)]] for i in range(0,int(vertexes))]).astype(int)
    df = df.groupby(['user_id'])['if_belong'].sum().reset_index(name ='number_of_places_available')
    print(df)
main()
    
