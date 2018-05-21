import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import json
import os
import re
import sys
import time

try:
    from urlparse import urljoin
    from urllib import urlretrieve
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import urlretrieve

CSS_EXPLORE = "a[href='/explore/']"
CSS_LOAD_MORE = "a._1cr2e._epyes"

# JAVASCRIPT COMMANDS
SCROLL_UP = "window.scrollTo(0, 0);"
SCROLL_DOWN = "window.scrollTo(0, document.body.scrollHeight);"
 
class InstagramScraper():
 
    def __init__(self):
        self.host = 'https://www.instagram.com/'
        self.driver = webdriver.Chrome()
        self.userNumber = 120
        self.maxPostNumPerUser = 500
        self.savePath = 'instagramDataset.txt'
        

    def login(self, authentication=None):
        """
            authentication: path to authentication json file
        """
        self.driver.get(urljoin(self.host, "accounts/login/"))

        if authentication:
            print("Username and password loaded from {}".format(authentication))
            with open(authentication, 'r') as fin:
                auth_dict = json.loads(fin.read())
            # Input username
            username_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            username_input.send_keys(auth_dict['username'])
            # Input password
            password_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            password_input.send_keys(auth_dict['password'])
            # Submit
            password_input.submit()
        else:
            print("Type your username and password by hand to login!")
            print("You have a minute to do so!")

        print("")
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_EXPLORE))
        )

 
    def getPostLinks(self):
        sdriver = self.driver
        try:
            self.driver.get(urljoin(self.host,"explore/"))
        except:
            return
        assert "Instagram" in self.driver.title
        time.sleep(2)
        self.scroll_to_num_of_posts(self.userNumber)
        postLinks = self.driver.find_elements_by_xpath("//div[contains(@class, '_mck9w _gvoze  _tn0ps')]")
        print("posts: {}".format(len(postLinks)))
        postLinksList = []
        for postLink in postLinks:
            postLinksList.append(postLink.find_element_by_css_selector('a').get_attribute('href'))
        # if len(postLinksList):
        #     print (postLinksList[0])

        return postLinksList
        
        # print (postLinks[0])

    def getUsers(self,postLinksList):
        userDict = {}
        for postLink in postLinksList:
            try:
                self.driver.get(postLink)
                userClass = self.driver.find_element_by_xpath("//div[contains(@class, '_eeohz')]")
                user = userClass.find_element_by_css_selector('a').text
                userLink = userClass.find_element_by_css_selector('a').get_attribute('href')
                #print (user)
                if user not in userDict:
                    userDict[user] = userLink
            except:
                continue

        return userDict

    def getPosts(self,userDict):
        f = open(self.savePath,'w')
        f.write("user\tpostsNum\tfollowersNum\tfollowingNum\thasLocation\tAtUserNum\tAtUserPostsNum\tAtUserFollowerNum\tAtUserFollowingNum\thashTagNum\thashTagPostsNum\tlikeNum\n")

        featureList = []
        j = 0
        for user in userDict:
            # print (userDict[user])
            try:
                self.driver.get(userDict[user])
            
                numsClass = self.driver.find_element_by_xpath("//ul[contains(@class, '_h9luf')]")
                nums = numsClass.find_elements_by_xpath("//span[contains(@class, '_fd86t')]")
                postsNum = nums[0].text
                followersNum = nums[1].text
                followingNum = nums[2].text
                # print (user)
                # print (postsNum)
                # print (followersNum)
                # print (followingNum)
                postLinkList = []
                
                i = 0
                self.scroll_to_num_of_posts(self.maxPostNumPerUser)
                postsClass = self.driver.find_elements_by_xpath("//div[contains(@class, '_mck9w _gvoze  _tn0ps')]")
                for postLink in postsClass:
                    link = postLink.find_element_by_css_selector('a').get_attribute('href')
                    postLinkList.append(link)

                    i += 1
                    if i >= self.maxPostNumPerUser:
                        break

                postsList = []
                for link in postLinkList:
                    time.sleep(0.5)
                    self.driver.get(link)
                    # print (link)

                    ifVideo = self.driver.find_elements_by_xpath("//a[contains(@class, '_qzesf')]")
                    if len(ifVideo) > 0:
                        continue
                    
                    # self.driver.get(link)
                    postDict = {}
                    likeNum = '0'
                    try:
                        likeNumClass = self.driver.find_element_by_xpath("//a[contains(@class, '_nzn1h')]")
                        likeNum = likeNumClass.find_element_by_css_selector('span').text             
                        postDict["likeNum"] = likeNum
                        # print (likeNum)
                    except:
                        continue 

                    hasLocation = '0'
                    try:
                        locationClass = self.driver.find_elements_by_xpath("//a[contains(@class, '_6y8ij')]")
                        if len(locationClass) > 0:
                            hasLocation = '1'
                    except:
                        print ("exception2")
                    postDict["hasLocation"] = hasLocation
                    

                    # AtUserClass =  self.driver.find_elements_by_xpath("//a[contains(@class, 'notranslate')]")
                    AtUserNum = '0'
                    AtUserPostsNum = ''
                    AtUserFollowerNum = ''
                    AtUserFollowingNum = ''
                    AtUserLinkList = []
                    # for userLink in AtUserClass:
                    #     link = userLink.get_attribute('href')
                    #     AtUserLinkList.append(link)

                    hashTagNum = 0
                    hashTagPostsNum = ''
                    hashTagList = []

                    CommetClass =  self.driver.find_element_by_xpath("//ul[contains(@class, '_b0tqa')]")
                    CommetClassList = CommetClass.find_elements_by_xpath("//li[contains(@class, '_ezgzd')]")
                    if len(CommetClassList) > 0:
                        try:
                            span = CommetClassList[0].find_element_by_css_selector('span')
                            ll = span.find_elements_by_css_selector('a')
                            for l in ll:
                                try:
                                    hashTagLink = l.get_attribute('href')
                                    if hashTagLink.find("/explore/tags/") >= 0:
                                        hashTagList.append(hashTagLink)
                                        # print (hashTagLink)
                                except:
                                    continue
                        except:
                            print ("exception1")
                    hashTagNum = str(len(hashTagList))

                    CommetClass =  self.driver.find_element_by_xpath("//ul[contains(@class, '_b0tqa')]")
                    CommetClassList = CommetClass.find_elements_by_xpath("//li[@class='_ezgzd']")
                    if len(CommetClassList) > 0:
                        try:
                            # print (len(CommetClassList))
                            # print (CommetClassList[0])
                            temp = CommetClassList[0]
                            AtUserSpan = temp.find_element_by_css_selector('span')
                            AtUserClass = AtUserSpan.find_elements_by_xpath("//a[@class='notranslate']")
                            for userLink in AtUserClass:
                                link = userLink.get_attribute('href')
                                AtUserLinkList.append(link)
                                # print (link)
                        except:
                            continue

                    AtUserNum = str(len(AtUserLinkList))
                        
                    for link in hashTagList:
                        time.sleep(0.5)
                        # print (link)
                        try:
                            self.driver.get(link)
                            nums = self.driver.find_element_by_xpath("//span[contains(@class, '_fd86t')]")
                            hashTagPostsNum += nums.text
                        except:
                            continue
                        

                    
                    for link in AtUserLinkList:
                        time.sleep(0.5)
                        try:
                            self.driver.get(link)
                            numsClass = self.driver.find_element_by_xpath("//ul[contains(@class, '_h9luf')]")
                            nums = numsClass.find_elements_by_xpath("//span[contains(@class, '_fd86t')]")
                            AtUserPostsNum += nums[0].text + ';'
                            AtUserFollowerNum += nums[1].text + ';'
                            AtUserFollowingNum += nums[2].text + ';'
                        except:
                            continue


                    fea = user + '\t' + postsNum + '\t' + followersNum + '\t' + followingNum + '\t' + hasLocation + \
                                    '\t' + AtUserNum + '\t' + AtUserPostsNum +  \
                                    '\t' + AtUserFollowerNum + '\t' + AtUserFollowingNum + \
                                    '\t' + hashTagNum + '\t' + hashTagPostsNum + \
                                    '\t' + likeNum + '\n'
                    f.write(fea)
                    # postDict["hashTagNum"] = hashTagNum
                    # postDict["hashTagPostsNum"] = hashTagPostsNum
                    # postDict["AtUserNum"] = AtUserNum
                    # postDict["AtUserPostsNum"] = AtUserPostsNum
                    # postDict["AtUserFollowerNum"] = AtUserFollowerNum
                    # postDict["AtUserFollowingNum"] = AtUserFollowingNum
                    # postsList.append(postDict)

                    # hashTagClass =  self.driver.find_elements_by_xpath("//a[contains(@class, 'notranslate')]")
                    # hashTagNum = len(hashTagClass)
                    # hashTagPostsNum = 0
                    # hashLinkList = []
                    # for hashTag in hashTagClass:
                    #     link = hashTag.get_attribute('href')
                    #     hashLinkList.append(link)
                    
                    # for link in hashLinkList:
                    #     self.driver.get(link)

                    # _b0tqa -> _ezgzd -> span         


                # featureDict = {}
                # featureDict["user"]= user
                # featureDict["postsNum"]= postsNum
                # featureDict["followersNum"]= followersNum
                # featureDict["followingNum"]= followingNum
                # featureDict["posts"] = postsList
                # featureList.append(featureDict)
                # j += 1
                # if j > 2:
                #     break
            except:
                continue

        f.close()

        return featureList

    
    def writeIntoFile(self,featureList):
        f = open(self.savePath,'w')
        f.write("user\tpostsNum\tfollowersNum\tfollowingNum\thasLocation\tAtUserNum\tAtUserPostsNum\tAtUserFollowerNum\tAtUserFollowingNum\thashTagNum\thashTagPostsNum\tlikeNum\n")
        for feature in featureList:
            featureCommon = feature["user"] + '\t' + feature["postsNum"] + '\t' + feature["followersNum"] + '\t' + \
            feature["followingNum"]
            for post in feature["posts"]:
                fea = featureCommon + '\t' + post['hasLocation'] + '\t' + post['AtUserNum'] + '\t' + post['AtUserPostsNum'] +  \
                '\t' + post['AtUserFollowerNum'] + '\t' + post['AtUserFollowingNum'] + \
                '\t' + post['hashTagNum'] + '\t' + post['hashTagPostsNum'] + \
                '\t' + post['likeNum'] + '\n'
                f.write(fea)
        
        f.close()


    def scroll_to_num_of_posts(self, number):
        # Get total number of posts of page
        postLinks = self.driver.find_elements_by_xpath("//div[contains(@class, '_mck9w _gvoze  _tn0ps')]")
        num_of_posts = len(postLinks)
        print("posts: {}, number: {}".format(num_of_posts, number))
        number = number if number < num_of_posts else num_of_posts

        num_to_scroll = int((number - 6) / 6) + 1
        for _ in range(num_to_scroll):
            self.driver.execute_script(SCROLL_DOWN)
            time.sleep(1)
            self.driver.execute_script(SCROLL_UP)
            time.sleep(0.2)

    def close(self):
        self.driver.close()
 

 
if __name__ == "__main__":
    test = InstagramScraper()
    test.login()
    postLinksList = test.getPostLinks()
    userDict = test.getUsers(postLinksList)
    featureList = test.getPosts(userDict)
    # test.writeIntoFile(featureList)
    # test.getPosts({"xxxx":"https://www.instagram.com/maddogracer4/"})
    test.close()

