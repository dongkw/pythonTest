package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"time"
)

func init() {
	http.HandleFunc("/signin/code", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "GET" {
			requestSigninCode(w, r)
		} else if r.Method == "POST" {
			checkSigninCode(w, r)
		} else {
			FailFunc(w, http.StatusMethodNotAllowed, http.StatusText(http.StatusMethodNotAllowed))
		}
	})
	http.HandleFunc("/sms/doctor", addDoctor)
	http.HandleFunc("/sms/doctor/audit", doctorAudit)
	http.HandleFunc("/sms/patient", bindPatient)
	http.HandleFunc("/sms/relatives/medication", medicationError)
	http.HandleFunc("/sms/relatives/review", reviewAlert)
	http.HandleFunc("/sms/relatives/medication/adjustment", medicationAdjustment)
}

// ## Request sms code by phone.
//
// ```
// GET /signin/code
// ```
//
// ### Parameters
//
// | Name       | Type   | Description  |
// |------------|--------|--------------|
// | phone      | string | **Required** |
//
// ### Response
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
//
// Rate Limit:
//
// ```json
// {
//    "data":{
//       "code":1,
//       "message":"rate limit is 1 per minute"
//    },
//    "status":"fail"
// }
// ```
func requestSigninCode(w http.ResponseWriter, r *http.Request) {
	phone := r.URL.Query().Get("phone")

	m, err := redis.HGetAllMap(phone)
	if err != nil {
		FailFunc(w, InternalError, err.Error())
		return
	}

	var (
		expired bool
		path    = r.URL.Path
	)
	if t, ok := m[path]; !ok {
		expired = true
	} else {
		if ts, _ := strconv.ParseInt(t, 10, 64); time.Now().Unix()-ts < 60 {
			FailFunc(w, SmsRateLimit, "rate limit is 1 per minute")
			return
		}
		redis.Del(phone)
		expired = true
	}
	if expired {
		if len(phone) > 0 {
			go func() {
				now, code := strconv.FormatInt(time.Now().Unix(), 10), codeSum()
				param := fmt.Sprintf(`{"code":"%v"}`, code)
				logToSentry(fmt.Sprintf("Your phone number: %s, sms code: %s", phone, code))
				println("sms code is : " + code)
				if _, err := redis.HmSet(phone, map[string]string{path: now, code: now}); err == nil {
					retryFunc(func() error {
						if ok, err := sendSms(param, "SMS_13043145", phone); !ok {
							return err
						}
						return nil
					}, 3)
				}
			}()
		}
	}

	OKFunc(w, M{})
}

// ## Check sms code along with phone.
//
// ```
// POST /signin/code
// ```
//
// ### Parameters
//
// | Name       | Type   | Description  |
// |------------|--------|--------------|
// | code       | string | **Required** |
// | phone      | string | **Required** |
// | consume    | bool   | Optional     |
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
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
//
// Code Not Found:
//
// ```json
// {
//    "data":{
//       "code":2,
//       "message":"code not found"
//    },
//    "status":"fail"
// }
// ```
func checkSigninCode(w http.ResponseWriter, r *http.Request) {
	var cd struct {
		Code    string `form:"code"`
		Phone   string `form:"phone"`
		Consume bool   `form:"consume"`
	}
	if err := json.NewDecoder(r.Body).Decode(&cd); err != nil {
		FailFunc(w, InternalError, err.Error())
		return
	}

	m, err := redis.HGetAllMap(cd.Phone)
	if err != nil {
		FailFunc(w, InternalError, err.Error())
		return
	}
	var expired bool
	if _, ok := m[cd.Code]; !ok {
		expired = true
	} else {
		if ts, _ := strconv.ParseInt(m[cd.Code], 10, 64); time.Now().Unix()-ts > 10*60 {
			go redis.Del(cd.Phone)
			expired = true
		}
	}
	if expired {
		FailFunc(w, SmsCodeNotFound, "code not exists")
		return
	}
	if cd.Consume {
		go redis.Del(cd.Phone)
	}
	OKFunc(w, M{})
}

// ## Send sms when doctor added.
//
// ```
// GET /sms/doctor
// ```
//
// ### Parameters
//
// | Name         | Type   | Description  |
// |--------------|--------|--------------|
// | hospitalName | string | **Required** |
// | phone        | string | **Required** |
// | password     | string | **Required** |
//
// ### Response
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
func addDoctor(w http.ResponseWriter, r *http.Request) {
	values := r.URL.Query()
	hname := values.Get("hospitalName")
	user := values.Get("phone")
	pass := values.Get("password")
	if len(hname) == 0 || len(user) == 0 || len(pass) == 0 {
		FailFunc(w, http.StatusBadRequest, http.StatusText(http.StatusBadRequest))
		return
	}
	param := fmt.Sprintf(`{"hospitalName":"%v","user":"%v","pass":"%v"}`, hname, user, pass)
	logToSentry(fmt.Sprintf("hospitalName: %v, user: %v, pass: %v", hname, user, pass))
	go retryFunc(func() error {
		_, err := sendSms(param, "SMS_59775086", user)
		return err
	}, 3)

	OKFunc(w, M{})
}

// ## Send sms when patient binded.
//
// ```
// GET /sms/patient
// ```
//
// ### Parameters
//
// | Name         | Type   | Description  |
// |--------------|--------|--------------|
// | hospitalName | string | **Required** |
// | phone        | string | **Required** |
// | doctorName   | string | **Required** |
//
// ### Response
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
func bindPatient(w http.ResponseWriter, r *http.Request) {
	values := r.URL.Query()
	hname := values.Get("hospitalName")
	user := values.Get("phone")
	dname := values.Get("doctorName")
	if len(hname) == 0 || len(user) == 0 || len(dname) == 0 {
		FailFunc(w, http.StatusBadRequest, http.StatusText(http.StatusBadRequest))
		return
	}
	param := fmt.Sprintf(`{"hospitalName":"%v","doctorName":"%v"}`, hname, dname)
	logToSentry(fmt.Sprintf("hospitalName: %v, doctorName: %v", hname, dname))
	go retryFunc(func() error {
		_, err := sendSms(param, "SMS_56015313", user)
		return err
	}, 3)

	OKFunc(w, M{})
}

// ## Send medication error sms to relatives and friend of patient.
//
// ```
// GET /sms/relatives/medication
// ```
//
// ### Parameters
//
// | Name         | Type   | Description  |
// |--------------|--------|--------------|
// | name         | string | **Required** |
// | phone        | string | **Required** |
//
// ### Response
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
func medicationError(w http.ResponseWriter, r *http.Request) {
	values := r.URL.Query()
	pname := values.Get("name")
	user := values.Get("phone")
	if len(pname) == 0 || len(user) == 0 {
		FailFunc(w, http.StatusBadRequest, http.StatusText(http.StatusBadRequest))
		return
	}
	param := fmt.Sprintf(`{"name":"%v"}`, pname)
	logToSentry(fmt.Sprintf("name: %v", pname))
	go retryFunc(func() error {
		_, err := sendSms(param, "SMS_82085010", user)
		return err
	}, 3)

	OKFunc(w, M{})
}

// ## Send review alert sms to relatives and friend of patient.
//
// ```
// GET /sms/relatives/review
// ```
//
// ### Parameters
//
// | Name         | Type   | Description  |
// |--------------|--------|--------------|
// | name         | string | **Required** |
// | phone        | string | **Required** |
// | time         | string | **Required** |
// | treatment    | string | **Required** |
// | period       | string | **Required** |
// | reference    | string | **Required** |
// | content      | string | **Required** |
//
// ### Response
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
func reviewAlert(w http.ResponseWriter, r *http.Request) {
	values := r.URL.Query()
	pname := values.Get("name")
	user := values.Get("phone")

	if len(pname) == 0 || len(user) == 0 {
		FailFunc(w, http.StatusBadRequest, http.StatusText(http.StatusBadRequest))
		return
	}
	param := fmt.Sprintf(`{"name":"%v"}`, pname)
	logToSentry(fmt.Sprintf(`"name":"%v"`, pname))
	go retryFunc(func() error {
		_, err := sendSms(param, "SMS_81985045", user)
		return err
	}, 3)

	OKFunc(w, M{})
}

// ## Send  sms to relatives and friend of patient.
//
// ```
// GET /sms/relatives/medication/adjustment
// ```
//
// ### Parameters
//
// | Name         | Type   | Description  |
// |--------------|--------|--------------|
// | name         | string | **Required** |
// | phone        | string | **Required** |
//
// ### Response
//
// ```json
// {
//	"data":{},
//	"status":"success"
// }
// ```
//
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
func medicationAdjustment(w http.ResponseWriter, r *http.Request) {
	values := r.URL.Query()
	pname := values.Get("name")
	user := values.Get("phone")
	if len(pname) == 0 || len(user) == 0 {
		FailFunc(w, http.StatusBadRequest, http.StatusText(http.StatusBadRequest))
		return
	}
	param := fmt.Sprintf(`{"name":"%v"}`, pname)
	logToSentry(fmt.Sprintf(`"name":"%v"`, pname))
	go retryFunc(func() error {
		_, err := sendSms(param, "SMS_82055017", user)
		return err
	}, 3)

	OKFunc(w, M{})
}

// ## Doctor audit.
//
// ```
// POST /sms/doctor/audit
// ```
//
// ### Parameters
//
// | Name       | Type   | Description  |
// |------------|--------|--------------|
// | phone      | string | **Required** |
// | isApproved | bool   | **Required** |
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
// Internal Error:
//
// ```json
// {
//    "data":{
//       "code":0,
//       "message":"xxx"
//    },
//    "status":"fail"
// }
// ```
//
// Code Not Found:
//
// ```json
// {
//    "data":{
//       "code":2,
//       "message":"code not found"
//    },
//    "status":"fail"
// }
// ```
func doctorAudit(w http.ResponseWriter, r *http.Request) {
	var f struct {
		Phone      string `form:"phone"`
		IsApproved bool   `form:"isApproved"`
	}
	if err := json.NewDecoder(r.Body).Decode(&f); err != nil {
		FailFunc(w, InternalError, err.Error())
		return
	}

	var template string

	if f.IsApproved {
		template = "SMS_85525042"
	} else {
		template = "SMS_85415061"
	}

	if _, err := sendSms("", template, f.Phone); err != nil {
		FailFunc(w, InternalError, err.Error())
		return
	}

	OKFunc(w, M{})
}
