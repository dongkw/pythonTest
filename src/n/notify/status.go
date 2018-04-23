package main

import "net/http"

func init() {
	http.HandleFunc("/status", status)
}

func status(w http.ResponseWriter, r *http.Request) {
	JSONFunc(w, M{"status": "UP"})
}
