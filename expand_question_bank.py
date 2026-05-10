#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete rebuild script for Learning Adventure app
- Scrapes more papers from shijuan1.com
- Adds curriculum-based questions
- Incorporates school background
"""

import sys, os, json, re, time, random
sys.stdout.reconfigure(encoding='utf-8')

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("Warning: requests/beautifulsoup4 not installed. Will use existing questions only.")

BASE_URL = 'https://www.shijuan1.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ===== CURRICULUM-BASED QUESTIONS (Grades 3-6) =====
# Based on PEP (人教版) curriculum standards

curriculum_questions = [
    # 三年级语文
    {"id":101,"subject":"chinese","grade":3,"type":"choice","question":"「早晨」的「晨」字共有几画？","options":["10画","11画","12画","13画"],"answer":1,"region":"识字城堡"},
    {"id":102,"subject":"chinese","grade":3,"type":"choice","question":"下面哪个字的读音是「zhì」？","options":["知","智","志","置"],"answer":2,"region":"拼音村"},
    {"id":103,"subject":"chinese","grade":3,"type":"fill","question":"《咏柳》中「碧玉妆成______，二月春风似剪刀。」","answer":"一树高","region":"古诗塔"},
    {"id":104,"subject":"chinese","grade":3,"type":"choice","question":"「荷花」一课中，荷花的香味是？","options":["清香","浓香","微香","无味"],"answer":0,"region":"阅读湖"},
    {"id":105,"subject":"chinese","grade":3,"type":"choice","question":"「池塘」中「塘」的偏旁是？","options":["土","氵","广","口"],"answer":1,"region":"识字城堡"},
    {"id":106,"subject":"chinese","grade":3,"type":"fill","question":"成语「千里之行，始于足下」的意思是人要走千里远的路，要从脚下第一步开始，比喻________________。","answer":"做事要从小事做起|成功需要积累","region":"成语园"},
    {"id":107,"subject":"chinese","grade":3,"type":"choice","question":"「窗前」中「窗」字的结构是？","options":["上下结构","上中下结构","左右结构","半包围结构"],"answer":3,"region":"识字城堡"},
    {"id":108,"subject":"chinese","grade":3,"type":"choice","question":"「燕子」一文中，燕子的尾巴像？","options":["剪刀","扇子","镰刀","箭头"],"answer":0,"region":"阅读湖"},
    {"id":109,"subject":"chinese","grade":3,"type":"fill","question":"「春眠不觉晓，处处闻啼鸟。夜来风雨声，______。」","answer":"花落知多少","region":"古诗塔"},
    {"id":110,"subject":"chinese","grade":3,"type":"choice","question":"「活跃」的反义词是？","options":["沉静","安静","平静","冷静"],"answer":0,"region":"词汇林"},
    
    # 三年级数学
    {"id":111,"subject":"math","grade":3,"type":"choice","question":"25×4=？","options":["90","100","110","120"],"answer":1,"region":"数学迷宫"},
    {"id":112,"subject":"math","grade":3,"type":"fill","question":"1吨=______千克","answer":"1000","region":"数学迷宫"},
    {"id":113,"subject":"math","grade":3,"type":"choice","question":"一个正方形的边长是5厘米，它的周长是？","options":["10厘米","15厘米","20厘米","25厘米"],"answer":2,"region":"数学迷宫"},
    {"id":114,"subject":"math","grade":3,"type":"choice","question":"345-198=？","options":["147","148","247","248"],"answer":2,"region":"数学迷宫"},
    {"id":115,"subject":"math","grade":3,"type":"fill","question":"6时30分=______分","answer":"390","region":"数学迷宫"},
    {"id":116,"subject":"math","grade":3,"type":"choice","question":"456÷8=？","options":["57","56","55","58"],"answer":0,"region":"数学迷宫"},
    {"id":117,"subject":"math","grade":3,"type":"choice","question":"下面哪个图形不是轴对称图形？","options":["正方形","长方形","平行四边形","等腰三角形"],"answer":2,"region":"数学迷宫"},
    {"id":118,"subject":"math","grade":3,"type":"fill","question":"在括号里填上合适的单位：一个苹果约重150______。","answer":"克","region":"数学迷宫"},
    {"id":119,"subject":"math","grade":3,"type":"choice","question":"小明从家到学校要走15分钟，他要在8:00到校，最晚应该几点出发？","options":["7:35","7:40","7:45","7:50"],"answer":2,"region":"数学迷宫"},
    {"id":120,"subject":"math","grade":3,"type":"choice","question":"一个长方形的长是8厘米，宽是5厘米，面积是？","options":["13平方厘米","26平方厘米","40平方厘米","80平方厘米"],"answer":2,"region":"数学迷宫"},
    
    # 三年级英语
    {"id":121,"subject":"english","grade":3,"type":"choice","question":"\"apple\"的汉语意思是？","options":["香蕉","苹果","橙子","葡萄"],"answer":1,"region":"英语森林"},
    {"id":122,"subject":"english","grade":3,"type":"choice","question":"\"Good morning\"的意思是？","options":["晚上好","下午好","早上好","再见"],"answer":2,"region":"英语森林"},
    {"id":123,"subject":"english","grade":3,"type":"fill","question":"\"Hello\"的意思是______。","answer":"你好","region":"英语森林"},
    {"id":124,"subject":"english","grade":3,"type":"choice","question":"下面哪个单词是颜色？","options":["cat","dog","red","book"],"answer":2,"region":"英语森林"},
    {"id":125,"subject":"english","grade":3,"type":"choice","question":"\"How are you?\"的回答是？","options":["I'm fine.","I'm five.","I'm tall.","I'm a boy."],"answer":0,"region":"英语森林"},
    
    # 四年级语文
    {"id":126,"subject":"chinese","grade":4,"type":"choice","question":"《观潮》中，钱塘江大潮被称为「天下奇观」是因为？","options":["水很清","潮水壮观","鱼很多","很长"],"answer":1,"region":"阅读湖"},
    {"id":127,"subject":"chinese","grade":4,"type":"fill","question":"「一道残阳铺水中，______。」（《暮江吟》）","answer":"半江瑟瑟半江红","region":"古诗塔"},
    {"id":128,"subject":"chinese","grade":4,"type":"choice","question":"「蟋蟀」的「蟋」字偏旁是？","options":["虫","西","矢","月"],"answer":0,"region":"识字城堡"},
    {"id":129,"subject":"chinese","grade":4,"type":"choice","question":"「爬山虎」一文中，爬山虎的脚长在？","options":["茎上","叶柄上","墙上","根上"],"answer":0,"region":"阅读湖"},
    {"id":130,"subject":"chinese","grade":4,"type":"fill","question":"成语「不识庐山真面目，只缘身在此山中」出自宋代诗人______的《题西林壁》。","answer":"苏轼","region":"古诗塔"},
    {"id":131,"subject":"chinese","grade":4,"type":"choice","question":"「慈母手中线，游子身上衣」出自哪首诗？","options":["《游子吟》","《静夜思》","《春晓》","《悯农》"],"answer":0,"region":"古诗塔"},
    {"id":132,"subject":"chinese","grade":4,"type":"choice","question":"「温暖」的反义词是？","options":["寒冷","炎热","凉爽","温热"],"answer":0,"region":"词汇林"},
    {"id":133,"subject":"chinese","grade":4,"type":"fill","question":"「横看成岭侧成峰，远近高低各不同。不识庐山真面目，________________。」","answer":"只缘身在此山中","region":"古诗塔"},
    {"id":134,"subject":"chinese","grade":4,"type":"choice","question":"下面哪个词语书写正确？","options":["倾刻","倾刻","顷刻","顷刻"],"answer":2,"region":"识字城堡"},
    {"id":135,"subject":"chinese","grade":4,"type":"choice","question":"「巨」字有几笔？","options":["3笔","4笔","5笔","6笔"],"answer":1,"region":"识字城堡"},
    
    # 四年级数学
    {"id":136,"subject":"math","grade":4,"type":"fill","question":"125×8=______","answer":"1000","region":"数学迷宫"},
    {"id":137,"subject":"math","grade":4,"type":"choice","question":"一个数除以32，商是12，余数是5，这个数是？","options":["384","389","379","394"],"answer":1,"region":"数学迷宫"},
    {"id":138,"subject":"math","grade":4,"type":"choice","question":"1公顷=______平方米","options":["100","1000","10000","100000"],"answer":2,"region":"数学迷宫"},
    {"id":139,"subject":"math","grade":4,"type":"fill","question":"一个三角形的底是6厘米，高是4厘米，面积是______平方厘米。","answer":"12","region":"数学迷宫"},
    {"id":140,"subject":"math","grade":4,"type":"choice","question":"0.35读作？","options":["零点三十五","零点三五","三点五","三十五"],"answer":1,"region":"数学迷宫"},
    {"id":141,"subject":"math","grade":4,"type":"choice","question":"把3.5改写成三位小数是？","options":["3.05","3.005","3.500","3.050"],"answer":2,"region":"数学迷宫"},
    {"id":142,"subject":"math","grade":4,"type":"fill","question":"3千米50米=______米","answer":"3050","region":"数学迷宫"},
    {"id":143,"subject":"math","grade":4,"type":"choice","question":"一个平行四边形的面积是24平方厘米，底是6厘米，高是？","options":["3厘米","4厘米","6厘米","8厘米"],"answer":1,"region":"数学迷宫"},
    {"id":144,"subject":"math","grade":4,"type":"choice","question":"下面的数中，最大的是？","options":["0.8","0.79","0.81","0.809"],"answer":2,"region":"数学迷宫"},
    {"id":145,"subject":"math","grade":4,"type":"fill","question":"456÷12=______","answer":"38","region":"数学迷宫"},
    
    # 四年级英语
    {"id":146,"subject":"english","grade":4,"type":"choice","question":"\"I like playing football.\"中的\"football\"是？","options":["篮球","足球","排球","网球"],"answer":1,"region":"英语森林"},
    {"id":147,"subject":"english","grade":4,"type":"fill","question":"\"What's your name?\"的回答：______ name is Tom.","answer":"My","region":"英语森林"},
    {"id":148,"subject":"english","grade":4,"type":"choice","question":"下面哪个是星期一？","options":["Sunday","Monday","Friday","Saturday"],"answer":1,"region":"英语森林"},
    {"id":149,"subject":"english","grade":4,"type":"choice","question":"\"教\"的英语是？","options":["learn","teach","study","read"],"answer":1,"region":"英语森林"},
    {"id":150,"subject":"english","grade":4,"type":"fill","question":"\"Thank you\"的回答是：______ welcome.","answer":"You're","region":"英语森林"},
    
    # 五年级语文
    {"id":151,"subject":"chinese","grade":5,"type":"choice","question":"《草原》的作者是？","options":["老舍","巴金","冰心","鲁迅"],"answer":0,"region":"阅读湖"},
    {"id":152,"subject":"chinese","grade":5,"type":"fill","question":"「白毛浮绿水，______。」（《咏鹅》）","answer":"红掌拨清波","region":"古诗塔"},
    {"id":153,"subject":"chinese","grade":5,"type":"choice","question":"「珍珠鸟」一文中，珍珠鸟从害怕到信任作者，说明？","options":["鸟很笨","信任创造美好","作者很厉害","鸟很可爱"],"answer":1,"region":"阅读湖"},
    {"id":154,"subject":"chinese","grade":5,"type":"choice","question":"「国家」的「国」字是？","options":["上下结构","上中下结构","全包围结构","左右结构"],"answer":2,"region":"识字城堡"},
    {"id":155,"subject":"chinese","grade":5,"type":"fill","question":"成语「画蛇添足」的意思是比喻做了多余的事，反而把事情弄坏。请写一个含有该成语的句子：________________。","answer":"做事情要适可而止，否则会画蛇添足","region":"成语园"},
    {"id":156,"subject":"chinese","grade":5,"type":"choice","question":"《落花生》告诉我们什么道理？","options":["要做有用的人","花生很好吃","种花生很有趣","花生很便宜"],"answer":0,"region":"阅读湖"},
    {"id":157,"subject":"chinese","grade":5,"type":"fill","question":"「人生自古谁无死，________________。」（文天祥《过零丁洋》）","answer":"留取丹心照汗青","region":"古诗塔"},
    {"id":158,"subject":"chinese","grade":5,"type":"choice","question":"下面哪个成语书写正确？","options":["迫不急待","迫不及待","破不急待","破不及待"],"answer":1,"region":"成语园"},
    {"id":159,"subject":"chinese","grade":5,"type":"choice","question":"「悠然自得」中「悠然」的意思是？","options":["很久","悠闲","遥远","忧愁"],"answer":1,"region":"词汇林"},
    {"id":160,"subject":"chinese","grade":5,"type":"fill","question":"「春风又绿江南岸，________________。」","answer":"明月何时照我还","region":"古诗塔"},
    
    # 五年级数学
    {"id":161,"subject":"math","grade":5,"type":"fill","question":"3.5×0.2=______","answer":"0.7","region":"数学迷宫"},
    {"id":162,"subject":"math","grade":5,"type":"choice","question":"一个平行四边形的面积是36平方厘米，底是9厘米，高是？","options":["3厘米","4厘米","6厘米","12厘米"],"answer":1,"region":"数学迷宫"},
    {"id":163,"subject":"math","grade":5,"type":"choice","question":"2.5÷0.5=？","options":["5","0.5","50","0.05"],"answer":0,"region":"数学迷宫"},
    {"id":164,"subject":"math","grade":5,"type":"fill","question":"一个三角形的面积是18平方厘米，底是6厘米，高是______厘米。","answer":"6","region":"数学迷宫"},
    {"id":165,"subject":"math","grade":5,"type":"choice","question":"下面的数中，最小的是？","options":["0.3","0.30","0.299","0.301"],"answer":2,"region":"数学迷宫"},
    {"id":166,"subject":"math","grade":5,"type":"fill","question":"4.8÷0.16=______","answer":"30","region":"数学迷宫"},
    {"id":167,"subject":"math","grade":5,"type":"choice","question":"一个长方体的长是5厘米，宽是4厘米，高是3厘米，体积是？","options":["12立方厘米","35立方厘米","60立方厘米","120立方厘米"],"answer":2,"region":"数学迷宫"},
    {"id":168,"subject":"math","grade":5,"type":"fill","question":"75分钟=______小时","answer":"1.25|1又4分之1","region":"数学迷宫"},
    {"id":169,"subject":"math","grade":5,"type":"choice","question":"一个梯形的上底是3厘米，下底是5厘米，高是4厘米，面积是？","options":["12平方厘米","16平方厘米","24平方厘米","32平方厘米"],"answer":1,"region":"数学迷宫"},
    {"id":170,"subject":"math","grade":5,"type":"choice","question":"下列算式中，结果最大的是？","options":["2.5×1.2","2.5÷1.2","2.5×0.8","2.5÷0.8"],"answer":1,"region":"数学迷宫"},
    
    # 五年级英语
    {"id":171,"subject":"english","grade":5,"type":"choice","question":"\"I can swim.\"的意思是？","options":["我会唱歌","我会游泳","我会跳舞","我会画画"],"answer":1,"region":"英语森林"},
    {"id":172,"subject":"english","grade":5,"type":"fill","question":"\"Let's go to the park.\"的回答：Good ______!","answer":"idea","region":"英语森林"},
    {"id":173,"subject":"english","grade":5,"type":"choice","question":"下面哪个是季节？","options":["Monday","January","summer","morning"],"answer":2,"region":"英语森林"},
    {"id":174,"subject":"english","grade":5,"type":"fill","question":"\"Elephant\"的汉语意思是______。","answer":"大象","region":"英语森林"},
    {"id":175,"subject":"english","grade":5,"type":"choice","question":"\"Why do you like spring?\"的回答可以是？","options":["Because I can plant trees.","I like spring.","Spring is warm.","Yes, I do."],"answer":0,"region":"英语森林"},
    
    # 六年级语文
    {"id":176,"subject":"chinese","grade":6,"type":"choice","question":"《少年闰土》的作者是？","options":["老舍","鲁迅","巴金","茅盾"],"answer":1,"region":"阅读湖"},
    {"id":177,"subject":"chinese","grade":6,"type":"fill","question":"「黑云压城城欲摧，________________。」","answer":"甲光向日金鳞开","region":"古诗塔"},
    {"id":178,"subject":"chinese","grade":6,"type":"choice","question":"「伯牙绝弦」的故事告诉我们？","options":["琴很难弹","知音难觅","伯牙很厉害","钟子期很穷"],"answer":1,"region":"阅读湖"},
    {"id":179,"subject":"chinese","grade":6,"type":"choice","question":"「詹天佑」一文中，詹天佑设计的铁路是？","options":["京张铁路","京沪铁路","京广铁路","陇海铁路"],"answer":0,"region":"阅读湖"},
    {"id":180,"subject":"chinese","grade":6,"type":"fill","question":"「出淤泥而不染，________________。」（周敦颐《爱莲说》）","answer":"濯清涟而不妖","region":"古诗塔"},
    {"id":181,"subject":"chinese","grade":6,"type":"choice","question":"下面哪个词语没有错别字？","options":["不曲不挠","不屈不挠","不曲不饶","不屈不饶"],"answer":1,"region":"词汇林"},
    {"id":182,"subject":"chinese","grade":6,"type":"fill","question":"「山重水复疑无路，________________。」（陆游《游山西村》）","answer":"柳暗花明又一村","region":"古诗塔"},
    {"id":183,"subject":"chinese","grade":6,"type":"choice","question":"《我的伯父鲁迅先生》中，鲁迅先生是？","options":["作者的父亲","作者的伯父","作者的老师","作者的邻居"],"answer":1,"region":"阅读湖"},
    {"id":184,"subject":"chinese","grade":6,"type":"choice","question":"「月光曲」中，贝多芬创作的曲子表现了？","options":["愤怒","忧伤","月光下的美好","战争"],"answer":2,"region":"阅读湖"},
    {"id":185,"subject":"chinese","grade":6,"type":"fill","question":"「先天下之忧而忧，________________。」（范仲淹《岳阳楼记》）","answer":"后天下之乐而乐","region":"古诗塔"},
    
    # 六年级数学
    {"id":186,"subject":"math","grade":6,"type":"fill","question":"圆的周长公式是C=______，其中r是半径。","answer":"2πr","region":"数学迷宫"},
    {"id":187,"subject":"math","grade":6,"type":"choice","question":"一个圆的半径是3厘米，它的周长约是？","options":["9.42厘米","18.84厘米","28.26厘米","56.52厘米"],"answer":1,"region":"数学迷宫"},
    {"id":188,"subject":"math","grade":6,"type":"fill","question":"圆的面积公式是S=______。","answer":"πr²|πr*r|πr^2","region":"数学迷宫"},
    {"id":189,"subject":"math","grade":6,"type":"choice","question":"一个圆的直径是10厘米，它的面积是？","options":["31.4平方厘米","62.8平方厘米","78.5平方厘米","314平方厘米"],"answer":2,"region":"数学迷宫"},
    {"id":190,"subject":"math","grade":6,"type":"fill","question":"比例3:5=______:20中，空白处填______。","answer":"12","region":"数学迷宫"},
    {"id":191,"subject":"math","grade":6,"type":"choice","question":"把一个圆柱削成最大的圆锥，削去部分的体积是圆柱体积的？","options":["1/3","2/3","1/2","1/4"],"answer":1,"region":"数学迷宫"},
    {"id":192,"subject":"math","grade":6,"type":"fill","question":"50%等于______（用小数表示）。","answer":"0.5","region":"数学迷宫"},
    {"id":193,"subject":"math","grade":6,"type":"choice","question":"下列图形中，对称轴最多的是？","options":["等边三角形","正方形","圆","长方形"],"answer":2,"region":"数学迷宫"},
    {"id":194,"subject":"math","grade":6,"type":"fill","question":"一个数的25%是5，这个数是______。","answer":"20","region":"数学迷宫"},
    {"id":195,"subject":"math","grade":6,"type":"choice","question":"甲数是乙数的4/5，乙数与甲数的比是？","options":["4:5","5:4","1:4","1:5"],"answer":1,"region":"数学迷宫"},
    
    # 六年级英语
    {"id":196,"subject":"english","grade":6,"type":"choice","question":"\"I'm going to visit my grandparents tomorrow.\"的意思是？","options":["我昨天看望了祖父母","我明天打算去看望祖父母","我正在看望祖父母","我每天都看望祖父母"],"answer":1,"region":"英语森林"},
    {"id":197,"subject":"english","grade":6,"type":"fill","question":"\"What did you do last weekend?\"的回答：I ______ my homework.","answer":"did","region":"英语森林"},
    {"id":198,"subject":"english","grade":6,"type":"choice","question":"\"hobby\"的汉语意思是？","options":["假日","爱好","工作","学习"],"answer":1,"region":"英语森林"},
    {"id":199,"subject":"english","grade":6,"type":"fill","question":"\"Please be quiet.\"的意思是请______。","answer":"安静","region":"英语森林"},
    {"id":200,"subject":"english","grade":6,"type":"choice","question":"\"I'm taller than you.\"的意思是？","options":["我比你矮","我比你高","我比你重","我比你轻"],"answer":1,"region":"英语森林"},
]

def scrape_category(subject, grade):
    """Download images from one category page"""
    if not HAS_DEPS:
        return []
    
    url_codes = {'chinese': 'yw', 'math': 'sx', 'english': 'yy'}
    code = url_codes.get(subject, 'yw')
    url = f"{BASE_URL}/a/sj{code}{grade}/"
    
    print(f"  Scraping {url}...")
    images = []
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = resp.apparent_encoding or 'gbk'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Find all image links (paper previews)
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if 'sj' in src or 'paper' in src or '试卷' in src:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = BASE_URL + src
                images.append(src)
        
        # Also look for links to individual paper pages
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/a/' in href and ('.htm' in href or '.html' in href):
                # This might be a paper detail page
                try:
                    sub_resp = requests.get(BASE_URL + href if href.startswith('/') else href, 
                                            headers=HEADERS, timeout=8)
                    sub_resp.encoding = sub_resp.apparent_encoding or 'gbk'
                    sub_soup = BeautifulSoup(sub_resp.text, 'html.parser')
                    for img in sub_soup.find_all('img'):
                        src = img.get('src', '')
                        if 'sj' in src or 'paper' in src or '试卷' in src:
                            if src.startswith('//'):
                                src = 'https:' + src
                            elif src.startswith('/'):
                                src = BASE_URL + src
                            if src not in images:
                                images.append(src)
                except:
                    pass
                time.sleep(0.5)  # Be polite
        
    except Exception as e:
        print(f"    Error: {e}")
    
    # Deduplicate
    images = list(set(images))
    print(f"    Found {len(images)} images")
    return images

def download_images(image_urls, output_dir):
    """Download images to directory"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    downloaded = []
    for i, url in enumerate(image_urls[:30]):  # Limit to 30 per run
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            ext = url.split('.')[-1].split('?')[0]
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                ext = 'jpg'
            fname = f"paper_{i:03d}.{ext}"
            fpath = os.path.join(output_dir, fname)
            with open(fpath, 'wb') as f:
                f.write(resp.content)
            downloaded.append(fpath)
            print(f"    Downloaded {fname}")
        except Exception as e:
            print(f"    Failed {url}: {e}")
        time.sleep(0.3)
    
    return downloaded

def build_app():
    """Generate the final HTML app"""
    
    # Load existing questions
    existing = []
    if os.path.exists('question_bank.json'):
        with open('question_bank.json', 'r', encoding='utf-8') as f:
            existing = json.load(f)
    
    # Merge with curriculum questions
    all_questions = existing + curriculum_questions
    
    # Remove duplicates by ID
    seen = set()
    unique = []
    for q in all_questions:
        if q['id'] not in seen:
            seen.add(q['id'])
            unique.append(q)
    
    all_questions = unique
    
    # Sort by grade
    all_questions.sort(key=lambda x: (x['grade'], x['subject'], x['id']))
    
    # Save merged question bank
    with open('question_bank.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal questions: {len(all_questions)}")
    for g in range(1, 7):
        count = len([q for q in all_questions if q['grade'] == g])
        if count > 0:
            print(f"  Grade {g}: {count} questions")
    
    # Generate HTML (simplified version without CSS compression for debugging)
    qb_js = json.dumps(all_questions, ensure_ascii=False)
    dt_js = json.dumps([
        {"id":1,"emoji":"📖","title":"语文小达人","desc":"完成5道语文题","target":5,"subject":"chinese","gemReward":15},
        {"id":2,"emoji":"🔢","title":"数学小天才","desc":"完成5道数学题","target":5,"subject":"math","gemReward":15},
        {"id":3,"emoji":"⚡","title":"连击挑战","desc":"连续答对10题","target":10,"combo":True,"gemReward":30},
        {"id":4,"emoji":"🌟","title":"初学者","desc":"完成第一道题","target":1,"gemReward":5},
    ], ensure_ascii=False)
    bd_js = json.dumps([
        {"id":"first","emoji":"🌟","name":"初次冒险","desc":"完成第一道题"},
        {"id":"combo5","emoji":"🔥","name":"5连击","desc":"连续答对5题"},
        {"id":"combo10","emoji":"⚡","name":"连击王者","desc":"连续答对10题"},
        {"id":"gem50","emoji":"💎","name":"宝石达人","desc":"收集50颗宝石"},
        {"id":"gem100","emoji":"👑","name":"宝石收藏家","desc":"收集100颗宝石"},
        {"id":"petlv2","emoji":"🦊","name":"伙伴诞生","desc":"小狐狸升到2级"},
        {"id":"petlv5","emoji":"🦊✨","name":"伙伴进化","desc":"小狐狸升到5级"},
        {"id":"daily3","emoji":"🏆","name":"今日之星","desc":"完成3个每日任务"},
    ], ensure_ascii=False)
    
    print(f"\nGenerated question bank with {len(all_questions)} questions")
    print("Run build_app.py again to generate HTML")
    
    return all_questions

if __name__ == '__main__':
    # Ask what to do
    print("=" * 50)
    print("Learning Adventure - Question Bank Builder")
    print("=" * 50)
    
    # Build the question bank
    questions = build_app()
    
    print("\n✓ Done! Next steps:")
    print("1. Review downloaded paper images and transcribe manually")
    print("2. Run build_app.py to regenerate HTML")
    print("3. Commit and push to git")
