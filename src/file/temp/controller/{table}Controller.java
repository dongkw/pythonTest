package cn.xinzhili.mis.controller;


import cn.xinzhili.medical.api.CoronaryStentInfo;
import cn.xinzhili.medical.api.response.CoronaryStentInfoListResponse;
import cn.xinzhili.mis.service.CoronaryStentService;
import cn.xinzhili.mis.util.AuthUtils;
import java.util.List;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

/**
 * @Author dkw[dongkewei@xinzhili.cn]
 * @data 2018/1/17 下午6:44
 */
@Controller
@RequestMapping("/stent")
public class CoronaryStentController {

  @Autowired
  private CoronaryStentService coronaryStentService;

  @GetMapping
  public String list(Model model, @Min(1) @RequestParam(defaultValue = "1") Integer pageAt,
      @Min(1) @Max(50) @RequestParam(defaultValue = "15") Integer pageSize, String name) {
    CoronaryStentInfoListResponse response = coronaryStentService
        .getCoronaryStentList(pageAt, pageSize, name);
    AuthUtils.populateUser2Model(model);
    List<CoronaryStentInfo> coronaryStentList = response.getCoronaryStentInfos();
    model.addAttribute("coronaryStentList", coronaryStentList);
    model.addAttribute("paging", true);
    model.addAttribute("pageAt", coronaryStentList.size() > 0 ? pageAt : 0);
    model.addAttribute("pageSize", pageSize);
    model.addAttribute("realSize", coronaryStentList.size());
    int total = response.getTotal();
    model.addAttribute("coronaryStentName", name);
    model.addAttribute("total", total);
    model.addAttribute("totalPage", (int) Math.ceil(total / (double) pageSize));
    return "coronary-stent-index";
  }

  @GetMapping("/{id}")
  public String getDetail(Model model, @PathVariable Long id) {
    AuthUtils.populateUser2Model(model);
    CoronaryStentInfo coronaryStentInfo = coronaryStentService.getCoronaryStentDetail(id);
    model.addAttribute("coronaryStent", coronaryStentInfo);
    return "coronary-stent-detail";
  }

  @PostMapping
  public String addCoronaryStent(Model model, CoronaryStentInfo coronaryStentInfo) {
    coronaryStentService.add(coronaryStentInfo);
    return "redirect:/stent";
  }

  @PostMapping("/{id}")
  public String updateCoronaryStent(Model model, CoronaryStentInfo coronaryStentInfo) {
    coronaryStentService.update(coronaryStentInfo);
    return "redirect:/stent";
  }

  @GetMapping("/new")
  public String toAddCoronaryStent(Model model) {
    AuthUtils.populateUser2Model(model);
    return "coronary-stent-add";
  }
}
