#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR/istasyonlar/istasyonlar_revize")

#Verinin okunması için kütüphaneler
import read_merge_nc as rmn
import plot as pl

#Uydu verilerinin konumları
import amasra_revize as amsr
import antalya_revize as antl
import arsuz_revize as arsz
import bozyazi_revize as bzyz
import erdemli_revize as erdm
import gokceada_revize as gada
import igneada_revize as iada
import maramra_ereglisi_revize as merg
import marmaris_revize as aksa
import mentes_revize as mnts
import trabzon_revize as trbz

#ALES VERİLERİ
#Aylık Veriler
##LRM VERİLERİ
ales_lrm_amsr_aylik = amsr.idw_lrm
ales_lrm_antl_aylik = antl.idw_lrm
ales_lrm_arsz_aylik = arsz.idw_lrm
ales_lrm_bzyz_aylik = bzyz.idw_lrm
ales_lrm_erdm_aylik = erdm.idw_lrm
ales_lrm_gada_aylik = gada.idw_lrm
ales_lrm_iada_aylik = iada.idw_lrm
ales_lrm_merg_aylik = merg.idw_lrm
ales_lrm_aksa_aylik = aksa.idw_lrm
ales_lrm_mnts_aylik = mnts.idw_lrm
ales_lrm_trbz_aylik = trbz.idw_lrm

##SAR VERİLERİ
ales_sar_amsr_aylik = amsr.idw_sar
ales_sar_antl_aylik = antl.idw_sar
ales_sar_arsz_aylik = arsz.idw_sar
ales_sar_bzyz_aylik = bzyz.idw_sar
ales_sar_erdm_aylik = erdm.idw_sar
ales_sar_gada_aylik = gada.idw_sar
ales_sar_iada_aylik = iada.idw_sar
ales_sar_merg_aylik = merg.idw_sar
ales_sar_aksa_aylik = aksa.idw_sar
ales_sar_mnts_aylik = mnts.idw_sar
ales_sar_trbz_aylik = trbz.idw_sar

#Excel tablosunun oluşturulması
ales_lrm_table_aylik = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/ales_lrm_aylik.xlsx",
                                   ales_lrm_amsr_aylik, ales_lrm_antl_aylik, ales_lrm_arsz_aylik, ales_lrm_bzyz_aylik, ales_lrm_erdm_aylik,
                                   ales_lrm_gada_aylik, ales_lrm_iada_aylik, ales_lrm_merg_aylik, ales_lrm_aksa_aylik, ales_lrm_mnts_aylik,
                                   ales_lrm_trbz_aylik)

ales_sar_table_aylik = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/ales_sar_aylik.xlsx",
                                   ales_sar_amsr_aylik, ales_sar_antl_aylik, ales_sar_arsz_aylik, ales_sar_bzyz_aylik, ales_sar_erdm_aylik,
                                   ales_sar_gada_aylik, ales_sar_iada_aylik, ales_sar_merg_aylik, ales_sar_aksa_aylik, ales_sar_mnts_aylik,
                                   ales_sar_trbz_aylik)

#GELENEKSEL VERİLER
#Aylık Veriler
##LRM VERİLERİ
gel_lrm_amsr_aylik = amsr.gel_idw_lrm
gel_lrm_antl_aylik = antl.gel_idw_lrm
gel_lrm_arsz_aylik = arsz.gel_idw_lrm
gel_lrm_bzyz_aylik = bzyz.gel_idw_lrm
gel_lrm_erdm_aylik = erdm.gel_idw_lrm
gel_lrm_gada_aylik = gada.gel_idw_lrm
gel_lrm_iada_aylik = iada.gel_idw_lrm
gel_lrm_merg_aylik = merg.gel_idw_lrm
gel_lrm_aksa_aylik = aksa.gel_idw_lrm
gel_lrm_mnts_aylik = mnts.gel_idw_lrm
gel_lrm_trbz_aylik = trbz.gel_idw_lrm

#Excel tablosunun oluşturulması
gel_lrm_table_aylik = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/gel_lrm_aylik.xlsx",
                                   gel_lrm_amsr_aylik, gel_lrm_antl_aylik, gel_lrm_arsz_aylik, gel_lrm_bzyz_aylik, gel_lrm_erdm_aylik,
                                   gel_lrm_gada_aylik, gel_lrm_iada_aylik, gel_lrm_merg_aylik, gel_lrm_aksa_aylik, gel_lrm_mnts_aylik,
                                   gel_lrm_trbz_aylik)

#Aylık Veriler
gel_sar_amsr_aylik = amsr.gel_idw_sar
gel_sar_antl_aylik = antl.gel_idw_sar
gel_sar_arsz_aylik = arsz.gel_idw_sar
gel_sar_bzyz_aylik = bzyz.gel_idw_sar
gel_sar_erdm_aylik = erdm.gel_idw_sar
gel_sar_gada_aylik = gada.gel_idw_sar
gel_sar_iada_aylik = iada.gel_idw_sar
gel_sar_merg_aylik = merg.gel_idw_sar
gel_sar_aksa_aylik = aksa.gel_idw_sar
gel_sar_mnts_aylik = mnts.gel_idw_sar
gel_sar_trbz_aylik = trbz.gel_idw_sar

#Excel tablosunun oluşturulması
gel_sar_table_aylik = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/gel_sar_aylik.xlsx",
                                   gel_sar_amsr_aylik, gel_sar_antl_aylik, gel_sar_arsz_aylik, gel_sar_bzyz_aylik, gel_sar_erdm_aylik,
                                   gel_sar_gada_aylik, gel_sar_iada_aylik, gel_sar_merg_aylik, gel_sar_aksa_aylik, gel_sar_mnts_aylik,
                                   gel_sar_trbz_aylik)





