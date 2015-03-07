package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
)

type Plivo struct {
	Host     string
	User     string
	Password string
}

func (p *Plivo) send(data map[string]string) {
	json_data, _ := json.Marshal(data)
	a, _ := http.NewRequest("POST", fmt.Sprintf("%s/%s/Message/", p.Host, p.User), bytes.NewReader(json_data))
	a.URL.User = url.UserPassword(p.User, p.Password)

	header := http.Header{}
	header.Add("Content-Type", "application/json")
	a.Header = header

	if false {
		var c http.Client
		resp, err := c.Do(a)
		if err != nil {
			fmt.Printf("Error >>> %s \n", err)
		} else {
			body, _ := ioutil.ReadAll(resp.Body)
			fmt.Printf("Resp >>> \n%s\n", body)
		}
	} else {
		fmt.Println(a, p)
	}
}

func main() {
	p := Plivo{
		Host:     "https://api.plivo.com/v1/Account",
		User:     "",
		Password: "",
	}

	data := map[string]string{
		"dst":  "",
		"src":  "",
		"text": "",
	}

	fmt.Println(p)
	p.send(data)
}
