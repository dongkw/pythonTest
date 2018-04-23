package cn.xinzhili.mis.service;

import cn.xinzhili.medical.api.CoronaryStentInfo;
import cn.xinzhili.medical.api.request.AddCoronaryStentRequest;
import cn.xinzhili.medical.api.request.UpdateCoronaryStentRequest;
import cn.xinzhili.medical.api.response.CoronaryStentInfoListResponse;
import cn.xinzhili.mis.client.MedicalServiceClient;
import cn.xinzhili.xutils.core.ErrorCode;
import cn.xinzhili.xutils.core.FailureException;
import cn.xinzhili.xutils.core.SystemException;
import cn.xinzhili.xutils.core.http.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * @Author dkw[dongkewei@xinzhili.cn]
 * @data 2018/2/27 下午2:37
 */
@Service
public class CoronaryStentService {
  private static final Logger logger = LoggerFactory.getLogger(CoronaryStentService.class);
  @Autowired 
  private MedicalServiceClient medicalServiceClient;
  public CoronaryStentInfoListResponse getCoronaryStentList(Integer pageAt, Integer pageSize, String name) {
    Response<CoronaryStentInfoListResponse> response = medicalServiceClient
        .getStentList(name, pageAt, pageSize);
    if (response.isFailed()) {
      logger.warn(" get coronaryStent list fail, response {}", response);
      throw new FailureException(response.getMessage());
    } else if (response.isError()) {
      logger.error("get coronaryStent list error, response {} ", response);
      throw new SystemException(ErrorCode.SERVER_ERROR);
    }
    return response.getDataAs(CoronaryStentInfoListResponse.class);

  }

  public CoronaryStentInfo getCoronaryStentDetail(long id) {
    Response<CoronaryStentInfo> response = medicalServiceClient.getStentById(id);
    if (response.isFailed()) {
      logger.warn(" get CoronaryStentInfo fail , response {}", response);
      throw new FailureException(response.getMessage());
    } else if (response.isError()) {
      logger.error("get CoronaryStentInfo error, response {} ", response);
      throw new SystemException(ErrorCode.SERVER_ERROR);
    }
    return response.getDataAs(CoronaryStentInfo.class);
  }

  public Response add(CoronaryStentInfo coronaryStentInfo) {
    AddCoronaryStentRequest request = new AddCoronaryStentRequest();
    BeanUtils.copyProperties(coronaryStentInfo, request);
    Response response = medicalServiceClient.addStent(request);
    if (response.isFailed()){
      logger.warn(" add coronaryStent fail , response {}", response);
      throw new FailureException(response.getMessage());
    } else if (response.isError()){
      logger.error("add coronaryStent error, response {} ", response);
      throw new SystemException(ErrorCode.SERVER_ERROR);
    }
    return response;
  }

  public Response update(CoronaryStentInfo basicHospitalInfo) {
    UpdateCoronaryStentRequest request = new UpdateCoronaryStentRequest();
    BeanUtils.copyProperties(basicHospitalInfo, request);
    Response response= medicalServiceClient.updateStent(request);
    if (response.isFailed()){
      logger.warn(" update CoronaryStent fail , response {}", response);
      throw new FailureException(response.getMessage());
    } else if (response.isError()){
      logger.error("update CoronaryStent error, response {} ", response);
      throw new SystemException(ErrorCode.SERVER_ERROR);
    }
    return response;
  }

}
