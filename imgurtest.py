from imgurpython import ImgurClient

PATH = "https://www.shardveil.com/images/cards/placeholder/arcanum-steward.png"

client = ImgurClient("ee1f0e6204e2e8d", "263d92665bb96cc79098637b79958f6a317f554f")

uploaded_image = client.upload_from_url(PATH)


print(uploaded_image['id'])