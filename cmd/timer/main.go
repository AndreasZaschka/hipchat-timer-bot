package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func handleGET(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi there, I have something for you, %s!", r.URL.Path[1:])
}

func handlePOST(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi there, I created something for you, %s!", r.URL.Path[1:])
}

func handler(w http.ResponseWriter, r *http.Request) {

	switch r.Method {
	case "POST":
		handlePOST
	default:
		handleGET
	}
    
}

func main() {
	port := os.Getenv("PORT")

	if port == "" {
		log.Fatal("$PORT must be set")
	}

	http.HandleFunc("/", handler)
    http.ListenAndServe(":" + port, nil)
}
