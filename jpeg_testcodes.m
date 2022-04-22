C = [9 9 9 9 9 9 9; 
      8 8 8 8 8 8 8; 
      7 7 7 7 7 7 7; 
      6 6 6 6 6 6 6; 
      5 5 5 5 5 5 5];
%C = C - 128;
C = fft2(C);   
display(abs(C))
Csort = sort(abs(C(:))); % Sort by magnitude;  shape: (mxn), 1
for keep =  [.1 .05 .01 .005]; %keep largest 10%, 5%, 1% .. of DCT coeffs
thresh = Csort( floor( (1-keep)*length(Csort) ) ); 
ind = abs(C)>thresh;
display(ind)
Cfilt = C.*ind; % Threshold small indices
display(Cfilt)
% Plot Reconstruction

end