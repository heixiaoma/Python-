#!/usr/bin/env python
# encoding: utf-8
import urllib.request
import re
import json
class Wz:
    def __init__(self, url,fl):
        UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
        req = urllib.request.Request(url, headers={'Cookie': cookie, 'User-Agent': UA})
        html = urllib.request.urlopen(req)
        str = html.read()
        if fl==1:
            data = str.decode('UTF-8')
        else:
            ss = bytes(str)
            data=ss.decode('unicode_escape')
        data = data.replace("\\", "")
        #标题
        rega = re.compile('<div class="WB_text W_f14" node-type="feed_list_content">.*? </div>',re.S)
        contents = rega.findall(data)
        regq = re.compile('<div class="WB_detail">(.*?)</div>',re.S)
        nick = regq.findall(data)
        for i in range(len(contents)):
            regqs = re.compile('nick-name=".*?"',re.S)
            s = regqs.findall(nick[i])
            #内容提取
            content=re.sub('<[^>]*>','',contents[i])
            nick_name=s[0][11:-1]
            if "展开全文" in content:
                self.getAll(contents[i],nick_name)
            else:
                #print(content)
                #print(nick_name)
                self.getfile(content, nick_name)

    def getAll(self,contents,nick_name):
         resg=re.compile('action-data="mid=.*?&is_settop',re.S)
         content=resg.findall(contents)
         mid=content[0][17:-10]
         content=self.gethttp(mid)
         self.getfile(content,nick_name)

    def gethttp(self,mid):
        UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
        urls="https://weibo.com/p/aj/mblog/getlongtext?&mid="+mid
        req = urllib.request.Request(urls, headers={'Cookie': cookie, 'User-Agent': UA})
        html = urllib.request.urlopen(req)
        str = html.read()
        data = str.decode('UTF-8')
        data_json = json.loads(data)
        if data_json['code'] == "100000":
            content = data_json["data"]["html"]
            content = re.sub('<[^>]*>', '', content)
            #print("mid："+content)
            return content
        else:
            print("数据失败")
            return "数据加载失败不能获取文本内容"
    def getfile(self,content,nick):
        f1=open(r'文章.txt','a',encoding='utf-8')
        f = open(r'作者.txt', 'a', encoding='utf-8')
        try:
            f1.write(content.strip() + '\n')
            f.write(nick.strip() + '\n')
        except:
            print("Error: 写入数据错一次")
        else:
            f.close()
            f1.close()
if __name__ == '__main__':
    page=input("获取多少页的数据")
    cookie="SINAGLOBAL=9475689197112.057.1500808137713; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7; _s_tentry=-; Apache=1145125992610.343.1514535461043; ULV=1514535461055:21:2:1:1145125992610.343.1514535461043:1512925850626; TC-V5-G0=26e4f9c4bdd0eb9b061c93cca7474bf2; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; login_sid_t=0b1b4a5adedab9d9892488771a4a2fcf; YF-V5-G0=3d0866500b190395de868745b0875841; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; wb_cusLike_6422008160=N; YF-Page-G0=35f114bf8cf2597e9ccbae650418772f; SCF=AmtWkdcvdIdoQTE_8av-cxp_m8IqR_DnsKyF6IxNO8BE3ANTs5WsfrHH-VEv1zW8jao8e2omgty_RRP_yhwCSa4.; SUHB=0cS3oDvqqpsWmB; un=15228311770; WBtopGlobal_register_version=49306022eb5a5f0b; SUB=_2AkMtGo8sdcPxrAVVmvoVzGPjao1H-jyez-baAn7uJhMyAxgv7mgyqSVutBF-XF4H64SO0p9HhRDej2y05kTATwmz; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhcrUDRGrJ2ipA6X-mViwPP5JpVF02feozRe02pS0M7; cross_origin_proto=SSL; WBStorage=c1cc464166ad44dc|undefined; UOR=cn.ui.vmall.com,widget.weibo.com,login.sina.com.cn; wb_cusLike_undefined=N"
    flag=1
    while flag<=int(page):
        url = 'https://weibo.com/p/1008089859a47560abd4a6d3f84612cd346358/emceercd?page='+str(flag)
        print("加载默认数据")
        Wz(url,1)
        url2="https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100808&page="+str(flag)+"&pagebar=1&tab=emceercd&pl_name=Pl_Third_App__46&id=1008089859a47560abd4a6d3f84612cd346358&script_uri=/p/1008089859a47560abd4a6d3f84612cd346358/emceercd&feed_type=1&pre_page="+str(flag)+"&domain_op=100808"
        print("加载隐藏数据")
        Wz(url2,2)
        print("数据第"+str(flag)+"页---完成")
        flag += 1