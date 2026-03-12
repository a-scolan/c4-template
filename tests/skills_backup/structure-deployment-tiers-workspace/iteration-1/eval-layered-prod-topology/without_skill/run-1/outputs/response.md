Je ferais trois grandes zones : une zone front, une zone applicative et une zone data.

Le gateway et les services métier peuvent aller côté front/app, RabbitMQ et le worker peuvent rester avec l'applicatif pour simplifier, puis MongoDB et MinIO dans la zone data. Le monitoring peut être ajouté à part si besoin.

Le point le plus important est de garder la base de données et le stockage non exposés directement à Internet ; seul le backend doit y accéder.