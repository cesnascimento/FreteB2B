import requests

cookies = {
  'cmbchkImpArJunto': '0',
  'cmbFilaImpressaoCorreios': '1',
  'cmbchkAutoFilaImpressaoCorreios': '1',
  'cmbFilaImpressaoPnet': '1',
  'cmbchkAutoFilaImpressaoPnet': '1',
  'cmbFilaImpressaoAr': '1',
  'cmbchkAutoFilaImpressaoAr': '1',
  'cmbFilaImpressaoAd': '1',
  'cmbOpcaoGerar': '1',
  'cmbchkAutoFilaImpressaoAd': '1',
  'OrdemDasColunasCheckList': 'IdxSts%2COptObj%2CDtaInc%2CStsObj%2CNrPnet%2CNomRem%2CCepRem%2CSMSRemetente%2CNomPos%2CCepPos%2CNomDes%2CLogDes%2CNroDes%2CCplDes%2CBrrDes%2CCidDes%2CUfxDes%2CAocDes%2CCepDes%2CTelDes%2CCelDes%2CEmlDes%2CDocDes%2CCttCar%2CSrvEct%2CEtqEct%2CPesObj%2CDimObj%2CAdcObj%2CVdcObj%2CVacObj%2CVolObj%2COb1Obj%2COb2Obj%2COb3Obj%2COb4Obj%2COb5Obj%2CNroNfe%2CCtdObj%2CVlrPos%2CPraPos%2CDtaPix%2CMotPix%2CNroPix%2CEmlPix%2CStsPix%2CFimPix%2CObsPix%2CDtaEnt%2CUniEnt%2CEndEnt%2CCepEnt%2CDtaPos%2CNomArq%2CNroPlp%2CEtkEct%2CNomArqAdx%2CRFID%2CStIncluirEmbalagemLR',
  'PHPSESSID': '1okr7198htgh6c9ggqmjr743k6',
}

headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'pt-BR,pt;q=0.6',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  # 'Cookie': 'cmbchkImpArJunto=0; cmbFilaImpressaoCorreios=1; cmbchkAutoFilaImpressaoCorreios=1; cmbFilaImpressaoPnet=1; cmbchkAutoFilaImpressaoPnet=1; cmbFilaImpressaoAr=1; cmbchkAutoFilaImpressaoAr=1; cmbFilaImpressaoAd=1; cmbOpcaoGerar=1; cmbchkAutoFilaImpressaoAd=1; OrdemDasColunasCheckList=IdxSts%2COptObj%2CDtaInc%2CStsObj%2CNrPnet%2CNomRem%2CCepRem%2CSMSRemetente%2CNomPos%2CCepPos%2CNomDes%2CLogDes%2CNroDes%2CCplDes%2CBrrDes%2CCidDes%2CUfxDes%2CAocDes%2CCepDes%2CTelDes%2CCelDes%2CEmlDes%2CDocDes%2CCttCar%2CSrvEct%2CEtqEct%2CPesObj%2CDimObj%2CAdcObj%2CVdcObj%2CVacObj%2CVolObj%2COb1Obj%2COb2Obj%2COb3Obj%2COb4Obj%2COb5Obj%2CNroNfe%2CCtdObj%2CVlrPos%2CPraPos%2CDtaPix%2CMotPix%2CNroPix%2CEmlPix%2CStsPix%2CFimPix%2CObsPix%2CDtaEnt%2CUniEnt%2CEndEnt%2CCepEnt%2CDtaPos%2CNomArq%2CNroPlp%2CEtkEct%2CNomArqAdx%2CRFID%2CStIncluirEmbalagemLR; PHPSESSID=1okr7198htgh6c9ggqmjr743k6',
  'Origin': 'https://vipp.visualset.com.br',
  'Referer': 'https://vipp.visualset.com.br/vipp/entradadados/FrmTriagem.php',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-GPC': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'dnt': '1',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
}


def headers_vipp(rastreio):
  data = {
      'limit': '10',
      'offset': '0',
      'order': 'asc',
      'sort': 'NomDes',
      'dtaini': '20230628',
      'dtafim': '20230629',
      'tipent': '0|',
      'stsobj': '',
      'idxpos': '',
      'comarx': '0',
      'comatx': '0',
      'comadx': '0',
      'naoimp': '1',
      'cometq': '0',
      'etqimp': '0',
      'arximp': '0',
      'cmpbusca': 'EtqEct',
      'lista': f'{rastreio}',
  }
  response = requests.post(
      'https://vipp.visualset.com.br/vipp/entradadados/FrmCheckList/ListarCheckList.php',
      cookies=cookies,
      headers=headers,
      data=data,
  ).json()
  dicionario = dict()
  rastreio = response['rows'][0]['EtqEct']
  nota_fiscal = response['rows'][0]['NroNfe']
  valor = float(response['rows'][0]['VlrPos'])
  dicionario[rastreio] = [nota_fiscal, valor]
  return dicionario