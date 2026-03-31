where source.tag is #next => prod:match canary:match
where source.tag is #web => prod:match canary:match
where source.tag is #gamma => prod:match canary:no
where source.tag is #canary => prod:no canary:match
where source.tag is #missing => prod:no canary:no
The deployment-instance tag rule is cumulative: each instance has the logical element's tags plus its own extra tags.
