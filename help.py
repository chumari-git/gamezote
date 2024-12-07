from dash import html
pathname = "/"

def update_output(pathname):
	children=[]
	if pathname == "/":
		for cells in range(10):
			children.append(html.Div(['Body box13'], className='cell box'))
	return children

print(update_output(pathname))

label = None
if label == None:
	print("mr")