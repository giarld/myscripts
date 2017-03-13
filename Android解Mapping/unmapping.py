#!/usr/bin/python
# coding=utf-8

import sys
import os

suffix = ".java"

class LogUnMapping:
    """Log UnMapping Class"""
    mappaingFileName = ""
    mappaing = []  # Mapping relations

    def __init__(self, mapFilePath):
        # print "Create Class"
        self.__loadMapping(mapFilePath)

    # load Mapping relations
    def __loadMapping(self, mapFilePath):
        self.mappaingFileName = mappingPath.split("/")[-1]
        print "load Mapping", self.mappaingFileName
        mapFile = open(mapFilePath, "r")
        mapMapping = {}
        lines = mapFile.readlines()
        for line in lines:
            if not line:
                continue
            if line.startswith("    ") or line.startswith("\t"):
                continue
            strs = line.split(" -> ")
            if len(strs) != 2:
                continue
            leftS = self.__trimStr(strs[0])
            rightS = self.__trimStr(strs[1])
            if leftS != rightS:
                mapMapping[rightS] = leftS
                # print rightS, "=", leftS

        self.mappaing = mapMapping.items()
        self.mappaing.sort(lambda x, y: cmp(len(x[0]), len(y[0])), reverse=True)
        print "Ok."
        # for _, __ in self.mappaing:
        #     os.system("echo '" + _ + " = " + __ + "' >> mapps")

    def __trimStr(self, text):
        if not text or text == "":
            return ""
        while True:
            pd = False
            if text.endswith("\n"):
                text = text[:-2]
                pd = True
            if text.endswith(":"):
                text = text[:-2]
                pd = True
            if text.endswith(" "):
                text = text[:-2]
                pd = True
            if not pd:
                break
        return text

    def __isLetter(self, chr):
        return chr.isalpha() or chr.isdigit()

    # work
    def unMapping(self, logFilePath):
        print "unMapping", logFilePath, "... "
        inFile = open(logFilePath, "r")
        outFile = open(logFilePath + suffix, "w")
        inLines = inFile.readlines()
        for line in inLines:
            currLine = line
            for map, ori in self.mappaing:
                index = currLine.find(map)
                if index != -1:
                    if index != 0 and self.__isLetter(currLine[index - 1]):
                        continue
                    if self.__isLetter(currLine[index + len(map)]):
                        continue
                    newLine = currLine[:index] + ori + currLine[index + len(map):]
                    currLine = newLine
            outFile.write(currLine)

        inFile.close()
        outFile.close()
        print "OK."

    def unMappingDirs(self, logDirPath):
        print "Start unMapping."
        for _, __, fileNames in os.walk(logDirPath):
            for fileName in fileNames:
                if self.mappaingFileName in fileName:
                    continue
                if suffix in fileName:
                    continue
                self.unMapping(os.path.join(_, fileName))


# Main
if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 2:
        print "错误：需要两个参数"
        print "参数1：mapping文件路径"
        print "参数2：日志目录路径"
        sys.exit(1)
    mappingPath = args[1]
    logDir = args[2]
    lum = LogUnMapping(mappingPath)
    lum.unMappingDirs(logDir)
