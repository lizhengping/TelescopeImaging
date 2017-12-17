import configparser

conf = configparser.ConfigParser()
conf.read("config.cfg")
sections = conf.sections()



def getConfig(option,section="default"):
    optionValue=[]
    if type(option)==type([]):
        for i in option:
            optionValue.append(eval(conf.get(section,i)))
        if len(optionValue)==1:
            return optionValue[0]
        else:
            return optionValue
    if type(option)==type('string'):
        return eval(conf.get(section,option))

def setConfig():
    # 写配置文件

    # 更新指定section, option的值
    conf.set("section2", "port", "8081")

    # 写入指定section, 增加新option的值
    conf.set("section2", "IEPort", "80")

    # 添加新的 section
    conf.add_section("new_section")
    conf.set("new_section", "new_option", "http://www.cnblogs.com/tankxiao")

    # 写回配置文件
    conf.write(open("c:\\test.conf", "w"))


if __name__ == '__main__':
    # 获取指定的section， 指定的option的值
    name = getConfig(["name"])
    print(name)
    name = getConfig("name")
    print(name)
    age = getConfig(["age"])
    print(age)


    #获取所有的section


