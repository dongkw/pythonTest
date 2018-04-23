package main

import (
	"encoding/json"
	"net/http"

	"git.xzlcorp.com/backend/csm/push"
)

func init() {
	http.HandleFunc("/push/bind", bindDevice)
	http.HandleFunc("/push/unbind", unBindDevice)
	http.HandleFunc("/push/notifies", pushNotify)
}

// ## Bind mobile device to push message.
//
// ```
// POST /push/bind
// ```
//
// ### Parameters
//
// | Name        | Type        | Description                                     |
// |-------------|-------------|-------------------------------------------------|
// | deviceToken | string      | **Required**  device id                         |
// | deviceType  | string      | **Required** `ios` or `android` const           |
// | subscriber  | string      | **Required** id or other unique identify        |
//
// ### Response
//
// Success:
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
func bindDevice(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		FailFunc(w, http.StatusMethodNotAllowed, http.StatusText(http.StatusMethodNotAllowed))
		return
	}
	f := struct {
		DeviceToken string `form:"deviceToken"`
		DeviceType  string `form:"deviceType"`
		Subscriber  string `form:"subscriber"`
	}{}

	err := json.NewDecoder(r.Body).Decode(&f)
	if err != nil || (f.DeviceType != "android" && f.DeviceType != "ios") || len(f.Subscriber) == 0 || !validSubscribes(f.Subscriber) {
		FailFunc(w, BadRequest, "bad request")
		return
	}

	if r, err := saveLC(f.DeviceType, f.DeviceToken, f.Subscriber); err == nil {
		retryFunc(func() error { return push.BindDevice(dbpool.NewSession(nil), f.DeviceType, f.DeviceToken, r.ObjectID) }, 3)
	}

	OKFunc(w, M{})
}

// ## Push notifies to receivers.
//
// ```
// POST /push/notifies
// ```
//
// ### Parameters
//
// | Name        | Type        | Description                                                                |
// |-------------|-------------|----------------------------------------------------------------------------|
// | title       | string      | **Optional** this notify title                                             |
// | alert       | string      | **Required** this notify content                                           |
// | content     | json(map)   | **Required** a json map contains notify info                               |
// | receivers   | string array| **Optional** receivers by their unique identifies                          |
// | deviceToken | string      | **Optional** device id                                                     |
//
// ### Response
//
// Success:
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
func pushNotify(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		FailFunc(w, http.StatusMethodNotAllowed, http.StatusText(http.StatusMethodNotAllowed))
		return
	}
	f := struct {
		Title       string                 `form:"title"`
		Alert       string                 `form:"alert"`
		Content     map[string]interface{} `form:"content"`
		Receivers   []string               `form:"receivers"`
		DeviceToken string                 `form:"deviceToken"`
	}{}

	if err := json.NewDecoder(r.Body).Decode(&f); err != nil || len(f.Alert) == 0 || len(f.Content) == 0 {
		goto fail
	}

	if len(f.Receivers) == 0 || !validSubscribes(f.Receivers...) {
		goto fail
	}

	retryFunc(func() error {
		_, err := pushLC(f.Title, f.Alert, f.Content, f.Receivers, f.DeviceToken)
		return err
	}, 3)

	OKFunc(w, M{})
	return
fail:
	{
		FailFunc(w, BadRequest, "bad request")
	}
}

// ## Unbind mobile device from leancloud.
//
// ```
// POST /push/unbind
// ```
//
// ### Parameters
//
// | Name        | Type        | Description                                     |
// |-------------|-------------|-------------------------------------------------|
// | deviceToken | string      | **Required**  device id                         |
// | subscriber  | string      | **Required** id or other unique identify        |
//
// ### Response
//
// Success:
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
func unBindDevice(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		FailFunc(w, http.StatusMethodNotAllowed, http.StatusText(http.StatusMethodNotAllowed))
		return
	}

	f := struct {
		DeviceToken string `form:"deviceToken"`
		Subscriber  string `form:"subscriber"`
	}{}

	if err := json.NewDecoder(r.Body).Decode(&f); err != nil || len(f.DeviceToken) == 0 || len(f.Subscriber) == 0 || !validSubscribes(f.Subscriber) {
		FailFunc(w, BadRequest, "bad request")
		return
	}

	objectID, err := push.UnbindDevice(dbpool.NewSession(nil), f.DeviceToken)
	if err == nil {
		retryFunc(func() error {
			_, err := unBindLC(objectID, f.Subscriber)
			return err
		}, 3)
	}

	OKFunc(w, M{})
}
