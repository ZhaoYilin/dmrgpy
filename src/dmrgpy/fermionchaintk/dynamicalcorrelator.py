import numpy as np
from .. import multioperator
from .. import operatornames
from . import mop


def get_dynamical_correlator_spinless(self,name="densitydensity",
        mode="DMRG",**kwargs):
    """
    Compute a dynamical correlator for a spinless chain
    """
    if mode=="DMRG":
        return self.get_dynamical_correlator_MB(name=name,**kwargs)
    elif mode=="ED":
        MBF = self.get_MBF() # get the object
        return MBF.get_dynamical_correlator(name=name,**kwargs)
    else: raise




def get_dynamical_correlator_spinful(self,name="densitydensity",
        i=0,j=0,**kwargs):
    """Return the dynamical correlator of an spinful system"""
    def getd(ii,jj):
        mi,mj= self.N[2*i+ii],self.N[2*i+jj]
        return self.get_dynamical_correlator_spinless(
            name=(mi,mj)**kwargs)
    def getcdc(ii,jj):
        mi,mj= self.Cdag[2*i+ii],self.C[2*i+jj]
        return self.get_dynamical_correlator_spinless(
                name=(mi,mj),**kwargs)
    def getccd(ii,jj):
        mi,mj= self.C[2*i+ii],self.Cdag[2*i+jj]
        return self.get_dynamical_correlator_spinless(
                name=(mi,mj)**kwargs)
    def getcc(ii,jj):
        mi,mj= self.C[2*i+ii],self.C[2*i+jj]
        return self.get_dynamical_correlator_spinless(
                name=(mi,mj),**kwargs)
    ### Worksround for four field operators
    def caca(ii,jj,kk,ll): # four field operators
        mi = self.Cdag[2*j+jj]*self.C[2*i+ii]
        mj = self.Cdag[2*j+kk]*self.C[2*i+ll]
        return self.get_dynamical_correlator_spinless(name=(mi,mj),
                **kwargs)
    def aaaa(ii,jj,kk,ll): # four field operators
        mi = self.Cdag[2*j+jj]*self.Cdag[2*i+ii]
        mj = self.C[2*j+kk]*self.C[2*i+ll]
        return self.get_dynamical_correlator_spinless(name=(mi,mj),
                **kwargs)
    if name=="densitydensity":
        (es,uu) = getd(0,0) # up up
        (es,ud) = getd(0,1) # up up
        (es,dd) = getd(1,1) # down down
        (es,du) = getd(1,0) # down down
        return (es,uu+dd+ud+du) # return the contributions
    elif name=="cdc":
        (es,uu) = getcdc(0,0)
        (es,dd) = getcdc(1,1)
        return (es,uu+dd) # return the contributions
    elif name=="ccd":
        (es,uu) = getccd(0,0)
        (es,dd) = getccd(1,1)
        return (es,uu+dd) # return the contributions
    elif name=="cc":
        (es,uu) = getcc(0,0)
        (es,dd) = getcc(1,1)
        return (es,uu+dd) # return the contributions
    elif name=="cdcup": return getcdc(0,0)
    elif name=="cdcdn": return getcdc(1,1)
    elif name=="ccdup": return getccd(0,0)
    elif name=="ccddn": return getccd(1,1)
    elif name=="ccup": return getcc(0,0)
    elif name=="ccdn": return getcc(1,1)
    elif name=="ZZ":
        mi = self.Sz[i]
        mj = self.Sz[j]
        return self.get_dynamical_correlator_spinless(name=(mi,mj),
                **kwargs)
    elif name=="XX":
        mi = self.Sx[i]
        mj = self.Sx[j]
        return self.get_dynamical_correlator_spinless(name=(mi,mj),
                **kwargs)
    elif name=="YY":
        mi = self.Sy[i]
        mj = self.Sy[j]
        return self.get_dynamical_correlator_spinless(name=(mi,mj),
                **kwargs)
    elif name=="SS": # return the SS dynamical correlator
        def getdsi(nn):
          return  get_dynamical_correlator_spinful(self,name=nn,i=i,j=j,**kwargs)
        (ex,dx) = getdsi("XX")
        (ey,dy) = getdsi("YY")
        (ey,dz) = getdsi("ZZ")
        return (ex,dx+dy+dz)
    elif name=="deltadelta": # swave pairing
        return aaaa(0,1,0,1) # return the swave pairing amplitude
    else: raise # not implemented




