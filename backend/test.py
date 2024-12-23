import requests


def download_image(url, save_as):
    response = requests.get(url)
    print(response)
    with open(save_as, "wb") as file:
        file.write(response.content)


image_url = "https://mmbiz.qpic.cn/sz_mmbiz_jpg/XWCwn2wOqYRegwEmn8E9UZV2uuZcTiaWK9WMjlqCortkmZto8Tkb0vSWMiaTgLD8Etjas7qBtj8ITy6icYH0rYibwQ/640?wx_fmt=jpeg&from=appmsg"
save_as = "./success1.jpg"

download_image(image_url, save_as)
