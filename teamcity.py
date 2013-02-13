import requests
import xml.etree.ElementTree as xml

class TeamCity:
    def __init__(self, url, username=None, password=None):
        self._auth = None
        if username is not None and password is not None:
            self._auth = requests.auth.HTTPBasicAuth(username, password)
        self.baseUrl = "%s/%s/app/rest"\
                % (url, "httpAutho" if self._auth else "guestAuth")

    def version(self):
        """ Returns the version of the REST plugin. """
        return self._getText("version")

    def projects(self):
        """ List all projects. """
        return self._attribs(self._getXml("projects"), "project")

    def project(self, id=None, name=None):
        """
        Get details for a specific project.
        Returns xml document.
        project(id="project131")
        project(name="MyProject")
        """
        # TODO create class representing xml document
        return self._getText("projects/" + self._projectLocator(id, name))

    def buildTypes(self, id=None, name=None):
        """
        List all build types or all build types belonging to a project.
        buildTypes()
        buildTypes(id="project131")
        buildTypes(name="MyProject")
        """
        what = "buildTypes"
        if id is not None or name is not None:
            what = "projects/" + self._projectLocator(id, name) + "/buildTypes"
        return self._attribs(self._getXml(what), "buildType")

    def buildType(self, id=None, name=None):
        """
        Get details for a specific buildType.
        Returns xml document.
        buildType(id="bt409")
        buildType(name="MyProject Trunk")
        """
        return self._getText("buildTypes/" + self._buildTypeLocator(id, name))

    def changes(self):
        return self._getXml("changes")

    def _projectLocator(self, id, name):
        return self._locator("project", id, name)

    def _buildTypeLocator(self, id, name):
        return self._locator("bt", id, name)

    def _locator(self, idPrefix, id, name):
        assert id is not None or name is not None
        if id is not None:
            # TODO implicit add prefix instead?
            if not id.startswith(idPrefix):
                raise ValueError(id, "needs %s prefix" % idPrefix)
            return "id:" + id
        if name is not None:
            return "name:" + name

    def _getText(self, what):
        url = self.baseUrl + "/" + what
        print("GET: " + url)
        return requests.get(url, auth=self._auth).text

    def _getXml(self, what):
        return xml.fromstring(self._getText(what).encode("utf-8"))

    def _attribs(self, xml, nodeName):
        return [i.attrib for i in xml.findall(nodeName)]

if __name__=="__main__":
    tc = TeamCity("http://teamcity.codebetter.com")
    print(tc.auth)
    print(tc.serverUrl)

