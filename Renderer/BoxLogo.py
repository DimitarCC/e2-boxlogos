from enigma import ePixmap
from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename, fileExists

def getLogoPath(logoType):
	def findLogo(logo):
		return (f := resolveFilename(SCOPE_GUISKIN, logo)) and fileExists(f) and f or ""
	if logoType == "model":
		if (f := findLogo("boxlogo.svg")):
			return f
		elif (f := findLogo("distrologo.svg")):
			return f
	elif logoType == "brand":
		return findLogo("brandlogo.svg")
	elif logoType == "distro":
		return findLogo("distrologo.svg")
	return ""

def getDefaultLogo(logoType, width, height):
		if logoType == "model":
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo.svg")
		elif logoType == "brand":
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo_small.svg")
		else:
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo.svg")

		is_svg = defaultLogoPath and defaultLogoPath.endswith(".svg")
		return defaultLogoPath and LoadPixmap(defaultLogoPath, width=width, height=0 if is_svg else height)

def setLogo(px, logoType, width, height):
	logoPath = getLogoPath(logoType)
	is_svg = logoPath and logoPath.endswith(".svg")
	pix = logoPath and LoadPixmap(logoPath, width=width, height=0 if is_svg else height)
	if pix:
		px.setPixmap(pix)
	else:
		defaultLogo = getDefaultLogo(logoType, width, height)
		if defaultLogo:
			px.setPixmap(defaultLogo)


class BoxLogo(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.logoType = "model"
		
	GUI_WIDGET = ePixmap

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == "logoType":
				self.logoType = value
				attribs.remove((attrib, value))
				break
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		pass
				
	def onShow(self):
		if self.instance:
			setLogo(self.instance, self.logoType, self.instance.size().width(), self.instance.size().height())
	