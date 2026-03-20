package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	resp, err := http.Get("https://estwarden.eu/api/threat-index")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()
	var d map[string]any
	json.NewDecoder(resp.Body).Decode(&d)
	fmt.Printf("%s — CTI: %.1f/100 (%s)\n", d["level"], d["score"], d["date"])
}
