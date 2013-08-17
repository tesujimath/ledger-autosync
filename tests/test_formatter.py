import ledgerautosync.formatter

from ofxparse import OfxParser

from unittest import TestCase
from mock import Mock

class TestFormatter(TestCase):
    def test_checking(self):
        ofx = OfxParser.parse(file('fixtures/checking.ofx'))
        formatter = ledgerautosync.formatter.Formatter(fid=ofx.account.institution.fid, acctid=ofx.account.account_id, currency=ofx.account.statement.currency, name="Foo")
        self.assertEqual(formatter.format_txn(ofx.account.statement.transactions[0]),
"""2011/03/31 DIVIDEND EARNED FOR PERIOD OF 03/01/2011 THROUGH 03/31/2011 ANNUAL PERCENTAGE YIELD EARNED IS 0.05%
  ; ofxid: 1101.1452687~7.0000486
  Foo                                          $0.01
  Expenses:Misc                               -$0.01
""")
        self.assertEqual(formatter.format_txn(ofx.account.statement.transactions[1]),
"""2011/04/05 AUTOMATIC WITHDRAWAL, ELECTRIC BILL WEB(S )
  ; ofxid: 1101.1452687~7.0000487
  Foo                                        -$34.51
  Expenses:Misc                               $34.51
""")
        self.assertEqual(formatter.format_txn(ofx.account.statement.transactions[2]),
"""2011/04/07 RETURNED CHECK FEE, CHECK # 319 FOR $45.33 ON 04/07/11
  ; ofxid: 1101.1452687~7.0000488
  Foo                                        -$25.00
  Expenses:Misc                               $25.00
""")

    def test_investments(self):
        ofx = OfxParser.parse(file('fixtures/fidelity.ofx'))
        formatter = ledgerautosync.formatter.Formatter(fid=ofx.account.institution.fid, acctid=ofx.account.account_id, currency=ofx.account.statement.currency, name="Foo")
        self.assertEqual(formatter.format_txn(ofx.account.statement.transactions[0]),
"""2012-07-20 04:00:00 YOU BOUGHT
  ; ofxid: 7776.01234567890.0123456789020201120120720
  Foo                                      100.00000 458140100 @ $25.635000000
  Foo                                      -$2563.50
""")