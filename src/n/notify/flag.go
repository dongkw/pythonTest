package main

import (
	"flag"
	"fmt"

	"github.com/douglarek/dbkit/dbc"
	"github.com/douglarek/dbkit/red"
	"github.com/gocraft/dbr"
	_ "github.com/lib/pq"
)

var (
	redisAddr string
	redis     *red.Redis

	driver, dsn string          // sql driver args.
	dbpool      *dbr.Connection // db connection pool.
	development bool
)

func init() {
	flag.StringVar(&redisAddr, "redis", "local-single.95gse5.0001.cnn1.cache.amazonaws.com.cn:6379", "redis address")
	flag.StringVar(&driver, "driver", "postgres", "database driver name")
	flag.StringVar(&dsn, "dns", "user=postgres password=postgres dbname=postgres sslmode=disable tcp=dev.cuauwtxtbfew.rds.cn-north-1.amazonaws.com.cn:5432", "database source name")
	flag.BoolVar(&development, "development", false, "development env")
	flag.Parse()

	redis = red.New(red.DefaultConfig().Merge(red.Config{Addr: redisAddr}))
	c, err := dbr.Open("postgres", "postgres:postgres@tcp(dev.cuauwtxtbfew.rds.cn-north-1.amazonaws.com.cn:5432)/dev", dbc.NewEventReceiver())
	if err != nil {
		fmt.Println(err)
	}
	dbpool = c
}
