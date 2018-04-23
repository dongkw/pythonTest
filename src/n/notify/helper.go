package main

import (
	"encoding/json"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/douglarek/apikit/push/lc"
	"github.com/douglarek/apikit/sms/alidayu"
	raven "github.com/getsentry/raven-go"
)

func init() {
	raven.SetDSN("https://55e01f677d6b421e84ec073ed1e3be8e:743a4521bed2429387c8f914dd932550@sentry.xinzhili.cn/4")
}

// Api return code
const (
	InternalError = iota // 0
	BadRequest

	SmsRateLimit
	SmsCodeNotFound
)

// JSONFunc renders a json response
func JSONFunc(w http.ResponseWriter, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(v)
}

// FailFunc renders a fail json response
func FailFunc(w http.ResponseWriter, code int, message string) {
	JSONFunc(w, M{"status": "fail", "data": M{"code": code, "message": message}})
}

// OKFunc renders a successful json response
func OKFunc(w http.ResponseWriter, data interface{}) {
	JSONFunc(w, M{"status": "success", "data": data})
}

// LC push related
const (
	LCAppID     = "5v2prFeaNJYNbFaUnrUQIdKu-gzGzoHsz"
	LCAppSecret = "Czytv8kFALRM38D0NIlp8vmw"
)

func sendSms(param, template string, phones ...string) (bool, error) {
	if development {
		return true, nil
	}
	a := alidayu.New(&http.Client{Timeout: 10 * time.Second})
	c := alidayu.DefaultConfig().Merge(
		alidayu.Config{AppKey: "23431585",
			RecNum:          strings.Join(phones, ","),
			SmsFreeSignName: "心之力",
			SmsParam:        param,
			SmsTemplateCode: template,
		})
	c.Sign = a.Sign(c, []byte("bfabd72ec3e37b8a6de2b8a215f5d72a"))
	j, err := a.SendSms(c)
	if err != nil {
		return false, err
	}
	return alidayu.SmsResult(j)
}

func codeSum() string {
	rand.Seed(time.Now().UnixNano())
	return strconv.Itoa(1e5 + rand.Intn(1e6-1e5) - 1)
}

func retryFunc(f func() error, count int) {
	for i := 0; i < count; i++ {
		if f() == nil {
			break
		}
	}
}

func saveLC(dtype, token string, channels ...string) (*lc.Resp, error) {
	s := lc.New(LCAppID, LCAppSecret)
	channels = append(channels, "all")
	r := lc.InstallationReq{DeviceType: dtype, DeviceToken: token, InstallationID: token, Channels: channels}
	return s.SaveInstallation(&r)
}

// M is an alias of map[string]interface{}.
type M map[string]interface{}

func pushLC(title, alert string, content map[string]interface{}, channels []string, installationID ...string) (*lc.Resp, error) {
	s := lc.New(LCAppID, LCAppSecret)
	r := lc.ChannelsReq{
		Prod: "dev",
		Data: M{
			"title":  title,
			"alert":  alert,
			"badge":  "1",
			"sound":  "default",
			"extra":  content,
			"action": "cn.xinzhili.service.PUSH_NOTIFY",
		}}
	r.Channels = channels
	if len(installationID) > 0 && len(installationID[0]) > 0 {
		r.Where = M{"installationId": installationID[0]}
	}
	return s.PushChannels(&r)
}

func unBindLC(objectID string, channels ...string) (*lc.Resp, error) {
	s := lc.New(LCAppID, LCAppSecret)
	r := lc.ChannelsOpsReq{
		Channels: struct {
			OP      string   `json:"__op"`
			Objects []string `json:"objects"`
		}{
			OP:      "Remove",
			Objects: channels},
	}
	return s.UnsubscribeChannel(objectID, &r)
}

func logToSentry(message string) {
	message = strings.Join([]string{message, ", ", time.Now().String()}, "")
	if development {
		packet := raven.NewPacket(message)
		packet.Level = raven.DEBUG
		raven.Capture(packet, map[string]string{"type": "sms"})
	}
}

// Sentry reports panic errors to sentry for each http request.
func Sentry(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		raven.CapturePanic(func() {
			next.ServeHTTP(w, r)
		}, map[string]string{"type": "panic"})
	})
}

func validSubscribes(subscribers ...string) bool {
	for _, r := range subscribers {
		r0 := string(r[0])
		// r0 -> "p" -> patient, "d" -> doctor
		if r0 != "d" && r0 != "p" {
			return false
		}
	}
	return true
}
