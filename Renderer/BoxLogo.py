from enigma import ePixmap, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER
from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename, fileExists

def getLogoPath(logoType):
	def findLogo(logo):
		return (f := resolveFilename(SCOPE_GUISKIN, logo)) and fileExists(f) and f or ""
	if logoType == "model":
		if (f := findLogo("logos/boxlogo.svg")):
			return f
		elif (f := findLogo("logos/distrologo.svg")):
			return f
	elif logoType == "brand":
		return findLogo("logos/brandlogo.svg")
	elif logoType == "distro":
		return findLogo("logos/distrologo.svg")
	return ""

def getDefaultLogo(logoType, width, height):
		if logoType == "model":
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo.svg")
		elif logoType == "brand":
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo_small.svg")
		else:
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo.svg")

		return detectAndFitPix(defaultLogoPath, width=width, height=height)

def detectAndFitPix(path, width, height, align):
	align_enum = RT_HALIGN_CENTER
	if align == "right":
		align_enum = RT_HALIGN_RIGHT
	elif align == "left":
		align_enum = RT_HALIGN_LEFT
	return path and LoadPixmap(path, width=width, height=height, scaletoFit=True, align=align_enum)


def setLogo(px, logoType, width, height, halign="center"):
	logoPath = getLogoPath(logoType)
	pix = detectAndFitPix(logoPath, width=width, height=height, align=halign)
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
		self.halign = "center"
		
	GUI_WIDGET = ePixmap

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == "logoType":
				self.logoType = value
				attribs.remove((attrib, value))
			elif attrib == "halign":
				self.halign = value
				attribs.remove((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		pass
				
	def onShow(self):
		if self.instance:
			x,y = self.position
			print("LOGO PosX: %d" % (x))
			setLogo(self.instance, self.logoType, self.instance.size().width(), self.instance.size().height(), self.halign)