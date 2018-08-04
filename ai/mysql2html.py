data_list = list()
for id in found:
    row = [customer_dict[id],("%.2f" % persent[id])]
    data_list.append(row)
#print(data_list)

df = pd.DataFrame(data_list,columns=['客户','found率'])
#s = df.style.applymap(color_negative_red)
#html = s.style.set_properties(**{'background-color': '#D2D8F9',
#                           'color': '#000000',
#                           'border-color': 'white'}).render()
#html = df.style.applymap(color_negative_red,subset=pd.IndexSlice[:, ['found率']]).render()
html = df.style.set_properties(**{'background-color': '#D2D8F9',
                           'color': '#000000',
                           'border-color': 'white'}).applymap(color_negative_red,subset=pd.IndexSlice[:, ['found率']]).render()
print(html)
