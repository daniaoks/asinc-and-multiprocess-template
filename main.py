
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time
import multiprocessing

url_list = ["https://www.olx.ua/d/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/nikolaev_106/?currency=UAH&search%5Border%5D=created_at%3Adesc", "https://www.olx.ua/d/uk/elektronika/kompyutery-i-komplektuyuschie/?currency=UAH&search%5Border%5D=created_at:desc", "https://www.olx.ua/d/uk/zhivotnye/ptitsy/", "https://www.olx.ua/d/uk/moda-i-stil/podarki/?utm_source=olx&utm_medium=virtual_category&utm_campaign=st_valentine_day", ] *25
chr = ['квартира', 'квартиру']


def find_str_item_in_title(title_item, chr):
    for chr_item in chr:
        if chr_item in title_item:
            chr_data = False
        else:
            chr_data = True
        return chr_data


async def get_page_data(session, page, url_olx, list_olx_title):

    if page >1:
        page_ = f"&page={page}"
        url_olx = url_olx + page_
    else:
        url_olx = url_olx
    async with session.get(url=url_olx) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")
        #main code parser
        title = soup.find_all(class_="css-16v5mdi er34gjf0")
        for title_item in title:
            list_olx_title.append(title_item.text)
            chr_data = find_str_item_in_title(title_item, chr)
            if chr_data == True:
                   list_olx_title.append(title_item.text)


async def create_task_olx(url_olx, list_olx_title):

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url_olx)
        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = soup.find("ul", class_="pagination-list").find_all("li")[-1].find("a").text

        tasks = []

        for page in range(1, int(pages_count) + 1):
            #create task get_page_data
            task = asyncio.create_task(get_page_data(session, page, url_olx, list_olx_title))
            tasks.append(task)
        await asyncio.gather(*tasks)


def run_async(url_olx):
    print(url_olx)
    list_olx_title = []
    asyncio.run(create_task_olx(url_olx, list_olx_title))

    return list_olx_title
def end_func(responce):
     print(time.time() - start_time)

    
if __name__ == '__main__':
    start_time = time.time()
    with multiprocessing.Pool(multiprocessing.cpu_count() *3) as p:
        p.map_async(run_async, url_list, callback=end_func)
        p.close()
        p.join()
        print(time.time() - start_time)







