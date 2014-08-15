from django.db import models
from datetime import datetime

# Create your models here.
class Common(models.Model):
    last_modified = models.DateTimeField(default=datetime.now())

    # meta info for the class.
    # abstract = True means it's an abstract class
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # always make sure we update timestamp on save
        # basically a trigger
        self.last_modified = datetime.now()

        # make sure we actually save
        super(Common, self).save(*args, **kwargs)

class Address(Common):
    street_name = models.CharField(max_length=50)
    street_number = models.IntegerField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    postal = models.CharField(max_length=10)

    @staticmethod
    def get_query(premnum):
        """ Gets the address for the given premise """
        return """SELECT ps.streetname AS street_name,
                   pp.house      AS street_number,
                   pt.townname   AS city,
                   pt.statecode  AS state,
                   pp.postalzone AS postal
            FROM   energydb.pm_premise pp
            INNER  JOIN energydb.pm_street ps ON ps.streetcode = pp.streetcode
            INNER  JOIN energydb.pm_town pt ON pt.towncode = pp.towncode
            WHERE  pp.premnum = {0}""".format(premnum)

class Debtor(Common):
    debtornum = models.IntegerField()
    firstname = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=30)
    company_code = models.CharField(max_length=4)
    on_ebill = models.CharField(max_length=1)
    phone_number = models.CharField(max_length=12, null=True)
    email_address = models.CharField(max_length=50, null=True)

    def get_absolute_url(self):
        return "/details/%s/" % self.debtornum

    @staticmethod
    def get_query(debtornum):
        """ Gets the details for the debtor """
        return """SELECT pc.firstnames,
                   pc.surname,
                   energy_onsite.get_company_code(pc.debtornum) AS company_code,
                   nvl(asn.use_email, 'N') as on_ebill,
                   pc.phone,
                   pc.email
            FROM   energydb.pm_consumer pc
            LEFT JOIN energydb.ar_stmt_notify asn on asn.debtornum = pc.debtornum
            WHERE consnum = 1 and pc.debtornum = {0}""".format(debtornum)

class Premise(Common):
    premnum = models.IntegerField()
    debtor = models.ForeignKey(Debtor)
    esiid = models.CharField(max_length=24, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.CharField(max_length=1, null=True)
    address = models.ForeignKey(Address, null=True)
    rate = models.ForeignKey("Rate", null=True)
    reading = models.ForeignKey("Reading", null=True)

    @staticmethod
    def get_query(debtornum):
        return """SELECT DISTINCT pec.premnum,
                            sdp.ext_sdp_code AS esiid,
                            pec.supplyreqdate as supply_date,
                            pec.status_cons AS status,
                            pec.finalreaddate as end_date
            FROM   energydb.pm_e_consprem pec
            INNER  JOIN energydb.pm_svc_deliv_pt svc ON svc.ref_no1 = pec.premnum
                                                        AND svc.sdp_type = 'P'
            INNER  JOIN energydb.pm_sdp_role sdp ON sdp.sdp_code = svc.sdp_code
                                                    AND sdp.participant_role = 'ESID'
            WHERE  pec.debtornum = {0}""".format(debtornum)

class Rate(Common):
    offer = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=5, decimal_places=4)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True)

    @staticmethod
    def get_query(debtornum, premnum):
        """ Gets the most recent rate for the debtor/premise """
        return  """SELECT DISTINCT eer.offering  AS offer,
                      ts.unitcharge AS rate,
                      pt.start_date AS effective_from,
                      pt.end_date   AS effective_to
      FROM   energydb.pm_e_consprem pec
      INNER  JOIN (SELECT p.*,
                          row_number() over(PARTITION BY premnum ORDER BY nvl(start_date, '31-DEC-2999') DESC) AS rate_rank
                   FROM   energydb.pm_tariff p) pt ON pt.premnum = pec.premnum
                                                      AND pt.rate_rank = 1
      INNER  JOIN energy_onsite.edi_ebt_rate eer ON eer.tariffclass = pt.tariffclass
      INNER  JOIN (SELECT tariffclass,
                          unitcharge,
                          row_number() over(PARTITION BY tariffclass ORDER BY date_effective DESC) AS rate_rank
                   FROM   energydb.tm_step) ts ON ts.tariffclass = pt.tariffclass
                                                  AND ts.rate_rank = 1
      WHERE  pec.debtornum = {0}
             AND pec.premnum = {1}""".format(debtornum, premnum)

class PTJ(Common):
    ptj_number = models.IntegerField()
    debtor = models.ForeignKey(Debtor, null=True)
    premise = models.ForeignKey(Premise, null=True)
    date_logged = models.DateTimeField()
    date_status = models.DateTimeField(null=True)
    type_code = models.CharField(max_length=2, null=True)
    class_code = models.CharField(max_length=10, null=True)
    subclass_code = models.CharField(max_length=2, null=True)
    status_code = models.CharField(max_length=2, null=True)

    @staticmethod
    def get_query(debtornum):
        return """SELECT prt_process_no,
                   prt_type_code,
                   prt_class_code,
                   prt_subclass_code,
                   prt_status_code,
                   premnum,
                   datetime_logged,
                   datetime_status
            FROM   (SELECT pp.prt_process_no,
                           pp.prt_type_code,
                           pp.prt_class_code,
                           pp.prt_subclass_code,
                           pp.prt_status_code,
                           pp.premnum,
                           pp.datetime_logged,
                           pp.datetime_status,
                           row_number() over(PARTITION BY pp.debtornum ORDER BY pp.datetime_logged DESC) AS prt_rank
                    FROM   energydb.prt_process pp
                    WHERE  debtornum = {0})
            WHERE  prt_rank <= 6""".format(debtornum)

class Invoice(Common):
    debtor = models.ForeignKey(Debtor, null=True)
    invoice_num = models.CharField(max_length=10, null=True)
    invoice_date = models.DateField(null=True)
    invoice_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    due_date = models.DateField(null=True)

    @staticmethod
    def get_query(debtornum):
        """ Gets the latest invoice for the debtor """
        return """SELECT invoice_num, invoice_date, invoice_amt, due_date
            FROM   (SELECT row_number() over(PARTITION BY debtornum ORDER BY date_r DESC) AS inv_rank,
                           ei.e_invnum AS invoice_num,
                           ei.date_r AS invoice_date,
                           ei.amt_invoice AS invoice_amt,
                           ei.duedate AS due_date
                    FROM   energydb.eb_invoice ei
                    WHERE  debtornum = {0})
            WHERE  inv_rank = 1""".format(debtornum)


class Payment(Common):
    debtor = models.ForeignKey(Debtor, null=True)
    date_received = models.DateField()
    payment_amt = models.DecimalField(max_digits=10, decimal_places=2)
    channel = models.CharField(max_length=20)

    @staticmethod
    def get_query(debtornum):
      """ Gets the latest payment for the debtor """
      return """SELECT b.date_received, b.recpt_amt, bp.payment_desc AS channel
          FROM   (SELECT bch.*,
                         row_number() over(PARTITION BY bch.debtornum ORDER BY bch.date_received DESC) AS payment_rank
                  FROM   energydb.bk_csh_hist bch
                  WHERE  debtornum = {0}) b
          INNER  JOIN energydb.bk_payment bp ON bp.payment_code = b.payment_code
          WHERE  payment_rank = 1""".format(debtornum)


class Reading(Common):
  reading = models.IntegerField()
  read_date = models.DateField()
  read_method = models.CharField(max_length=1)
  invoice_num = models.IntegerField()

  @staticmethod
  def get_query(debtornum, premnum):
    return """SELECT reading, readdate, read_method, invnum
      FROM   (SELECT er.reading,
                     er.readdate,
                     er.read_method,
                     er.e_invnum AS invnum,
                     row_number() over(PARTITION BY er.premnum ORDER BY er.readdate DESC) AS reading_rank
              FROM   energydb.pm_e_consprem pec
              INNER  JOIN energydb.eb_reading er ON er.premnum = pec.premnum
                                                    AND
                                                    er.readdate >= pec.supplyreqdate
                                                    AND er.readdate <=
                                                    nvl(pec.finalreaddate,
                                                            '31-DEC-2999')
              WHERE  pec.debtornum = {0}
                     AND pec.premnum = {1}) where reading_rank = 1""".format(debtornum, premnum)
