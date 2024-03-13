import urllib
from bs4 import BeautifulSoup
import networkx as nx  
import ssl 
from urllib.request import Request,urlopen
import requests
from pyvis.network import Network
from IPython.display import display, HTML
import threading
import warnings
warnings.filterwarnings("ignore")
def get_html(url):
    gcontext=ssl.SSLContext()
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    #req=urllib.request.urlopen(url,context=gcontext)
    f=requests.get(url,verify=False)
    soup=BeautifulSoup(f.text,"html.parser")
    url_title=soup.find_all("title")
    h_ref=soup.find_all("a")
    ref_tab=[]
    for link in h_ref:
        temp=link.get("href")
        try:   
          if(str(temp[0])=="h" and str(temp[1])=="t" and str(temp[2])=="t" and str(temp[3])=="p"):
            ref_tab.append(temp)
        except:
            ref_tab=None
            url_title=None            
            return ref_tab,url_title
    url_title=str(url_title).replace('<title>','')
    url_title=str(url_title).replace('</title>','')
    ref_tab = list(dict.fromkeys(ref_tab))
    return ref_tab,url_title
def url_loop(graph,ref_tab,url_title_prev,attributed_title_tab,depth):
    print("depth",depth)
    if(depth>1):
        return 
    else:
     for url in ref_tab:
        url=str(url)
        new_ref_tab,new_url_title=get_html(url)
        if(new_url_title==None or new_ref_tab==None):
             continue
        if(new_url_title in attributed_title_tab):
             continue
        else:
            attributed_title_tab.append(new_url_title)
        graph.add_edge(str(url_title_prev),str(new_url_title))
        print("Url_title",new_url_title) 
        url_loop(graph,new_ref_tab,new_url_title,attributed_title_tab,depth+1)
"""def massively_parallel(graph,ref_tab,url_title_prev,attributed_title_tab,depth):
    urls=ref_tab
    print("coucou")
    rs= (grequests.get(url) for url in urls)
    #response=grequests.map(rs)
    print(response)"""
def propagation(start_url):
    graph=nx.Graph()
    ref_tab,url_title_prev=get_html(start_url)
    #cool_tab=[ref_tab[0],ref_tab[1],ref_tab[2]]
    graph.add_node(str(url_title_prev))
    attributed_title_tab=[]
    #massively_parallel(graph,cool_tab,url_title_prev,attributed_title_tab,depth=0)
    url_loop(graph,ref_tab,url_title_prev,attributed_title_tab,depth=0)
    #nx.draw(graph,with_labels=True,font_weight='bold')
    net=Network()
    for node in graph.nodes:
        net.add_node(node)
    for edge in graph.edges:
        net.add_edge(edge[0], edge[1])  
    net.show_buttons(filter_=['physics'])
    #net.show("graph.html",notebook=False)
    net.save_graph("networkx-pyvis.html")
    HTML(filename="networkx-pyvis.html")
if __name__ == '__main__':
    propagation("https://www.reddit.com/r/okcopainattard/")