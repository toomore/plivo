package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
)

type Plivo struct {
	Host     string
	User     string
	Password string
}

func (p *Plivo) send(data map[string]string) {
	json_data, _ := json.Marshal(data)
	a, _ := http.NewRequest("POST", fmt.Sprintf("%s/%s/Message/", p.Host, p.User), strings.NewReader(string(json_data)))
	a.URL.User = url.UserPassword(p.User, p.Password)

	header := http.Header{}
	header.Add("Content-Type", "application/json")
	a.Header = header

	var c http.Client
	resp, err := c.Do(a)
	if err != nil {
		fmt.Printf("Error >>> %s \n", err)
	} else {
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Printf("Resp >>> \n%s\n", body)
	}
}

func main() {
	p := Plivo{
		Host:     "https://api.plivo.com/v1/Account",
		User:     "", //user_id
		Password: "", //user_password
	}

	data := map[string]string{
		"dst":  "",
		"src":  "",
		"text": "測試",
	}

	p.send(data)
}
