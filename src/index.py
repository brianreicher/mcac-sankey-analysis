import sankey

print(sankey.Sankey(desired_columns=['BeginDate', 'Nationality', 'Gender']).group_df())
