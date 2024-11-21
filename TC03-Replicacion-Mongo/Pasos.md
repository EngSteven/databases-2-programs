# Pasos para configurar los shards y sus réplicas 

## 1. Ejecute el siguiente comando para construir el docker compose: 
``` bash
docker compose up 
```

## 2. Configuración de los servidores de configuración (Config Servers)
Desde el contenedor **mongocfg1** ejecute la siguiente configuración:
``` js
rs.initiate({
    _id: "mongors1conf", 
    configsvr: true, 
    members: [
        { 
            _id : 0, 
            host : "mongocfg1" 
        },
        { 
            _id : 1, 
            host : "mongocfg2" 
        }, 
        { 
            _id : 2, 
            host : "mongocfg3" 
        }
    ]
})
```

## 3. Configuración del primer shard (Shard 1 de la Réplica 1)
Desde el contenedor **mongors1n1** ejecute la siguiente configuración:

``` js
rs.initiate({
    _id : "mongors1", 
    members: [
        { 
            _id : 0, 
            host : "mongors1n1" 
        },
        { 
            _id : 1, 
            host : "mongors1n2" 
        },
        { 
            _id : 2, 
            host : "mongors1n3" 
        }
    ]
})
```

## 4. Configuración del segundo shard (Shard 2 de la Réplica 1)
Desde el contenedor **mongors2n1** ejecute la siguiente configuración:

``` js
rs.initiate({
    _id : "mongors2", 
    members: [
        { 
            _id : 0, 
            host : "mongors2n1" 
        },
        { 
            _id : 1, 
            host : "mongors2n2" 
        },
        { 
            _id : 2, 
            host : "mongors2n3" 
        }
    ]
})
```

## 5. Configuración del tercer shard (Shard 3 de la Réplica 1)
Desde el contenedor **mongors3n1** ejecute la siguiente configuración:

``` js
rs.initiate({
    _id : "mongors3", 
    members: [
        { 
            _id : 0, 
            host : "mongors3n1" 
        },
        { 
            _id : 1, 
            host : "mongors3n2" 
        },
        { 
            _id : 2, 
            host : "mongors3n3" 
        }
    ]
})
```

## 6. Agregar los shards en el router
Desde el contenedor **mongors1** ejecute la siguiente agregación de shards:

``` js
sh.addShard("mongors1/mongors1n1")
sh.addShard("mongors2/mongors2n1")
sh.addShard("mongors3/mongors3n1")
```

## 7. Configuración de shard de colecciones
Desde el contenedor **mongors1** ejecute la configuración:

```js
sh.shardCollection(
  "red_social_viajes.usuarios",
  { nombre_usuario: 1 },
  false,
  {
    numInitialChunks: 5,
    collation: { locale: "simple" }
  }
)

sh.shardCollection(
  "red_social_viajes.posts",
  { usuario_id: 1 },
  false,
  {
    numInitialChunks: 5,
    collation: { locale: "simple" }
  }
)

sh.shardCollection(
  "red_social_viajes.comentarios",
  { post_id: 1 },
  false,
  {
    numInitialChunks: 5,
    collation: { locale: "simple" }
  }
)

sh.shardCollection(
  "red_social_viajes.likes_posts",
  { usuario_id: 1, post_id: 1},
  false,
  {
    numInitialChunks: 5,
    collation: { locale: "simple" }
  }
)

sh.shardCollection(
  "red_social_viajes.likes_comentario",
  { usuario_id: 1, comentario_id: 1},
  false,
  {
    numInitialChunks: 5,
    collation: { locale: "simple" }
  }
)

sh.shardCollection(
  "red_social_viajes.follows",
  { nombre_usuario: 1},
  false,
  {
    numInitialChunks: 5,
    collation: { locale: "simple" }
  }
)
```

## 8. Correr el archivo de datos de prueba
Después de configurar todo correctamente vaya al archivo **datos.ipynb** y ejecute cada bloque de código para poder probar los datos en los shards.
