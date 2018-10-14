# -*- encoding:utf-8 -*-
import itchat
import DoubanCrawler

@itchat.msg_register(itchat.content.TEXT, itchat.content.PICTURE)
def simple_reply(msg):
    global film_info_all
    if u'电影' in msg['Text']:
        douban_object.browser_hotopen()
        douban_object.cmd2ctg(msg['Text'])
        film_ctg_option = ' '.join(DoubanCrawler.film_ctg)
        itchat.send_msg('---请选择一种类型---\n' + film_ctg_option, msg['FromUserName'])

    elif msg['Text'] in DoubanCrawler.film_ctg:
            itchat.send_msg('正在查找' + msg['Text'] + '电影...', msg['FromUserName'])
            del DoubanCrawler.command_cache[:]
            DoubanCrawler.command_cache.append(msg['Text'])
            film_info_all = douban_object.browser_action_general_info(msg['Text'])
            itchat.send_msg('---按热度排序---\n' + '\n' + '\n'.join(DoubanCrawler.film_heat), msg['FromUserName'])
            itchat.send_msg('---按时间排序---\n' + '\n' + '\n'.join(DoubanCrawler.film_time), msg['FromUserName'])
            itchat.send_msg('---按评论排序---\n' + '\n' + '\n'.join(DoubanCrawler.film_rating), msg['FromUserName'])
    # user enters the name of the film, so crawl the detail info
    else:
        search_num = 0
        for x in film_info_all:
            if msg['Text'] in x:
                itchat.send_msg('正在查找' + msg['Text'] + '...', msg['FromUserName'])
                idx = film_info_all.index(x)
                if 0 <= idx < 10:
                    search_num = 1
                elif 10 <= idx < 20:
                    search_num = 2
                else:
                    search_num = 3
                break
        url_result = douban_object.browser_action_detail_info(search_num, msg['Text'])
        html_result = douban_object.download_detail_info_html(url_result)
        douban_object.parse_detail_info(html_result)
        itchat.send_msg('\n\n'.join(DoubanCrawler.film_detail), msg['FromUserName'])


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    douban_object = DoubanCrawler.Crawler()
    film_info_all = []
    itchat.run()

