
class Download {

    def call_admantx(api, name, idProfile):
         response = requests.get("http://preprod.integralads.com/"+ api)
         segments = []
         if response.text:
            json_object = json.loads(response.text)
            for segment in json_object["data"]:
                    segments.append(segment["segment.ias_code"])
         profile = createProfile(segments,name,idProfile)
         return profile


}