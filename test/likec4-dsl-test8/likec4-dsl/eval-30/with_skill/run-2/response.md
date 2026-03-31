where source.tag is #next => prod:match canary:match
where source.tag is #web => prod:match canary:match
where source.tag is #gamma => prod:match canary:no
where source.tag is #canary => prod:no canary:match
where source.tag is #missing => prod:no canary:no
Deployment-instance tag matching is cumulative: each instance matches both its own tags and the tags inherited from its logical source element.
